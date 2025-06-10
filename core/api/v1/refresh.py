from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas.token import Token, TokenRefresh
from core.api.deps import get_current_user
from core.database.db_helper import db_helper
from core.services.auth import create_access_token, verify_refresh_token, create_refresh_token
from core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])
get_db = db_helper.scoped_session_dependency

@router.post("/refresh", response_model=Token)
async def refresh(
    data: TokenRefresh,
    db: AsyncSession = Depends(get_db),
):
    """
    Accepts a valid refresh token and returns a new access token.
    """
    payload = verify_refresh_token(data.refresh_token)
    phone_number: str = payload.get("sub")
    if not phone_number:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    new_access = create_access_token(
        sub=phone_number,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    new_refresh_token = create_refresh_token(
        sub=phone_number,
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    return {"access_token": new_access, "token_type": "bearer", "refresh_token": new_refresh_token}
