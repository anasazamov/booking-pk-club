from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from datetime import datetime

from core.database.models.models import User
from core.schemas.user import UserCreate, UserUpdate
from core.services.auth import get_password_hash

async def get_user_by_phone(db: AsyncSession, phone: str) -> User | None:
    result = await db.execute(select(User).where(User.phone_number == phone))
    return result.scalar_one_or_none()

async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def list_users(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10
) -> list[User]:

    result = await db.execute(
        select(User)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    hashed_pwd = get_password_hash(user_in.password)
    db_user = User(
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        phone_number=user_in.phone_number,
        password_hash=hashed_pwd,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def update_user(db: AsyncSession, user_id: int, user_in: UserUpdate) -> User | None:
    values = user_in.dict(exclude_unset=True)
    if "password" in values:
        values["password_hash"] = get_password_hash(values.pop("password"))
    values["updated_at"] = datetime.utcnow()
    stmt = (
        update(User)
        .where(User.id == user_id)
        .values(**values)
        .execution_options(synchronize_session="fetch")
    )
    await db.execute(stmt)
    await db.commit()
    return await get_user_by_id(db, user_id)