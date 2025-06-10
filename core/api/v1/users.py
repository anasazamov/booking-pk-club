from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas.user import UserRead, UserUpdate
from core.crud.users import get_user_by_id, list_users, update_user
from core.api.deps import get_current_user
from core.database.db_helper import db_helper
from core.database.models.models import RoleEnum
get_db = db_helper.scoped_session_dependency

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserRead])
async def users_list(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max number of records to return"),
    db: AsyncSession = Depends(get_db),
    current=Depends(get_current_user),
):
    """
    Получить список пользователей с пагинацией (только для админа и владельца).
    """
    if current.role not in (RoleEnum.admin, RoleEnum.owner):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return await list_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current=Depends(get_current_user),
):

    if current.role not in (RoleEnum.admin, RoleEnum.owner):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.patch("/{user_id}", response_model=UserRead)
async def modify_user(
    user_id: int,
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current=Depends(get_current_user),
):

    if current.role not in (RoleEnum.admin, RoleEnum.owner):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    user = await update_user(db, user_id, data)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user