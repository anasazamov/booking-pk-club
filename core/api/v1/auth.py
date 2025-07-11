from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from core.crud.user import get_user_by_phone, create_user
from core.schemas.user import UserCreate, UserRead
from core.schemas.token import Token
from core.services.auth import verify_password, create_access_token, create_refresh_token
from core.database.db_helper import db_helper
from core.api.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead)
async def register(
    data: UserCreate,
    db: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    if await get_user_by_phone(db, data.phone_number):
        raise HTTPException(status_code=400, detail="Phone already registered")
    user = await create_user(db, data)
    return user

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user = await get_user_by_phone(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(sub=str(user.phone_number))
    refresh_token = create_refresh_token(sub=str(user.phone_number))
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/me", response_model=UserRead)
async def get_current_user(
    db: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user=Depends(get_current_user)
):
    """
    Returns the currently authenticated user.
    """
    return current_user
