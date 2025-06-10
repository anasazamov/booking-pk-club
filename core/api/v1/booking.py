from fastapi import APIRouter, Depends, HTTPException, status, Header, Query
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas.booking import (
    BookingCreate, BookingRead, BookingUpdate
)
from core.crud.booking import (
    get_booking, list_bookings,
    create_booking, update_booking, delete_booking
)
from core.api.deps import get_current_user
from core.database.models.models import RoleEnum
from core.database.db_helper import db_helper
get_db = db_helper.scoped_session_dependency

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.post(
    "/",
    response_model=BookingRead,
    status_code=status.HTTP_201_CREATED
)
async def post_booking(
    data: BookingCreate,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
    db: AsyncSession = Depends(get_db),
    current = Depends(get_current_user)
):
    """
    Create a new booking. Idempotent via `Idempotency-Key`.
    """
    booking = await create_booking(db, current.id, data, idempotency_key)
    return booking

@router.get(
    "/",
    response_model=List[BookingRead]
)
async def get_bookings(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current = Depends(get_current_user)
):
    """
    List bookings. Regular users see own, admin/owner see all.
    """
    user_id = None
    if current.role not in (RoleEnum.admin, RoleEnum.owner):
        user_id = current.id
    bookings = await list_bookings(db, user_id, skip=skip, limit=limit)
    return bookings

@router.patch(
    "/{booking_id}",
    response_model=BookingRead
)
async def patch_booking(
    booking_id: int,
    data: BookingUpdate,
    db: AsyncSession = Depends(get_db),
    current = Depends(get_current_user)
):
    """
    Update a booking (admin/owner only).
    """
    if current.role not in (RoleEnum.admin, RoleEnum.owner):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    booking = await update_booking(db, booking_id, data)
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    return booking

@router.delete(
    "/{booking_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def del_booking(
    booking_id: int,
    db: AsyncSession = Depends(get_db),
    current = Depends(get_current_user)
):
    """
    Delete a booking (admin/owner only).
    """
    if current.role not in (RoleEnum.admin, RoleEnum.owner):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    await delete_booking(db, booking_id)