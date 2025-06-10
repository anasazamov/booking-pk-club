from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, delete
from datetime import datetime

from core.database.models.models import Booking
from core.schemas.booking import BookingCreate, BookingUpdate

async def get_booking(db: AsyncSession, booking_id: int) -> Booking | None:
    result = await db.execute(select(Booking).where(Booking.id == booking_id))
    return result.scalar_one_or_none()

async def list_bookings(
    db: AsyncSession,
    user_id: int | None = None,
    skip: int = 0,
    limit: int = 10
) -> list[Booking]:
    stmt = select(Booking)
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
    # Idempotency: assume Booking.idempotency_key exists
    existing = await db.execute(
        select(Booking).where(
            Booking.user_id == user_id,
            Booking.idempotency_key == idempotency_key
        )
    )
    booking = existing.scalar_one_or_none()
    if booking:
        return booking
    # Create new booking
    booking = Booking(
        user_id=user_id,
        place_id=data.place_id,
        start_datetime=data.start_datetime,
        end_datetime=data.end_datetime,
        amount=data.amount,
        status="pending",
        idempotency_key=idempotency_key
    )
    db.add(booking)
    await db.commit()
    await db.refresh(booking)
    return booking

async def update_booking(
    db: AsyncSession,
    booking_id: int,
    data: BookingUpdate
) -> Booking | None:
    booking = await get_booking(db, booking_id)
    if not booking:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(booking, field, value)
    booking.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(booking)
    return booking

async def delete_booking(db: AsyncSession, booking_id: int) -> None:
    await db.execute(delete(Booking).where(Booking.id == booking_id))
    await db.commit()