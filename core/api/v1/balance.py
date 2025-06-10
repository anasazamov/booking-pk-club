from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal

from core.schemas.balance import BalanceRead, TopUpRequest, TopUpResponse
from core.crud.balance import get_user, topup_balance
from core.api.deps import get_current_user
from core.database.models.models import RoleEnum
from core.database.db_helper import db_helper
get_db = db_helper.scoped_session_dependency

router = APIRouter(prefix="", tags=["balance"])

@router.get("/balance", response_model=BalanceRead)
async def read_balance(
    db: AsyncSession = Depends(get_db),
    current=Depends(get_current_user)
):
    """Get full user data including current balance."""
    user = await get_user(db, current.id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.post(
    "/balance/topup",
    response_model=TopUpResponse
)
async def topup_user_balance(
    data: TopUpRequest,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
    db: AsyncSession = Depends(get_db),
    current=Depends(get_current_user)
):
    """
    Top-up user's balance. Idempotent via `Idempotency-Key` header.
    Only admin and owner can perform.
    """
    if current.role not in (RoleEnum.admin, RoleEnum.owner):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    user = await topup_balance(db, data.user_id, data.amount, idempotency_key)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user