from sqlalchemy.ext.asyncio import AsyncSession
from core.database.models import BalanceTransaction, Booking
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import Result

async def transactions_history(db: AsyncSession, user_id: int):
    stmt = (
        select(BalanceTransaction)
        .options(
            selectinload(BalanceTransaction.booking)
            .selectinload(Booking.place)
        )
        .where(BalanceTransaction.user_id == user_id)
        .order_by(BalanceTransaction.created_at.desc())
    )
    result = await db.execute(stmt)
    return result.scalars().all()