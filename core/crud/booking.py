from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from datetime import datetime

from core.database.models.models import Booking, BalanceTransaction, BookingStatus, User, TransactionType
from core.schemas.booking import BookingCreate, BookingUpdate
from fastapi.exceptions import HTTPException
from fastapi import status

async def get_booking(db: AsyncSession, booking_id: int) -> Booking | None:
    result = await db.execute(select(Booking).options(selectinload(Booking.place)).where(Booking.id == booking_id))
    return result.scalar_one_or_none()

async def list_bookings(
    db: AsyncSession,
    user_id: int | None = None,
    skip: int = 0,
    limit: int = 10
) -> list[Booking]:
    stmt = select(Booking).options(selectinload(Booking.place))
    if user_id is not None:
        stmt = stmt.where(Booking.user_id == user_id)
    stmt = stmt.offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def create_booking(
    db: AsyncSession,
    user_id: int,
    data: BookingCreate,
    idempotency_key: str
) -> Booking:

    res = await db.execute(
        select(Booking)
        .where(Booking.user_id == user_id, Booking.idempotency_key == idempotency_key)
    )
    existing = res.scalar_one_or_none()
    if existing:
        return existing

     
        
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.balance < data.amount:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail="Insufficient balance")


    overlap_stmt = (
        select(Booking)
        .where(
            Booking.place_id == data.place_id,
            Booking.status != TransactionType.CANCELLED,
            Booking.start_datetime <= data.end_datetime,
            Booking.end_datetime >= data.start_datetime
        )
    )
    overlap = (await db.execute(overlap_stmt)).scalars().all()
    if overlap:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Place is already booked for this time")

    user.balance -= data.amount
    freeze_txn = BalanceTransaction(
        user_id=user_id,
        booking_id=None,  
        type=TransactionType.FREEZE,
        amount=data.amount,
        idempotency_key=idempotency_key,
    )
    db.add(freeze_txn)

    booking = Booking(
        user_id=user_id,
        place_id=data.place_id,
        start_datetime=data.start_datetime,
        end_datetime=data.end_datetime,
        amount=data.amount,
        status=BookingStatus.PENDING,
        idempotency_key=idempotency_key,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(booking)

    freeze_txn.booking_id = booking.id
    await db.commit()  

    await db.refresh(booking, attribute_names=["place"])
    return await get_booking(db, booking_id=booking.id)

async def update_booking(
    db: AsyncSession,
    booking_id: int,
    data: BookingUpdate
) -> Booking | None:
    booking = await get_booking(db, booking_id)
    if not booking:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(booking, field, value)
    booking.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(booking)
    return booking

async def delete_booking(db: AsyncSession, booking_id: int) -> None:
    await db.execute(delete(Booking).where(Booking.id == booking_id))
    await db.commit()

# async def booking_list_for_admin(
#         db: AsyncSession
# ):
#     stmt = select(Booking).options(selectinload(Booking.user)).options(selectinload(Booking.place)).group_by(Booking.user_id)
#     db.execute