from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal

from core.database.models.models import User, BalanceTransaction, TransactionType

async def get_user(db: AsyncSession, user_id: int) -> User | None:

    return await db.get(User, user_id)

async def get_transaction_by_key(db: AsyncSession, key: str) -> BalanceTransaction | None:
    result = await db.execute(
        select(BalanceTransaction).where(BalanceTransaction.idempotency_key == key)
    )
    return result.scalar_one_or_none()

async def topup_balance(
    db: AsyncSession,
    user_id: int,
    amount: Decimal,
    idempotency_key: str
) -> User | None:
    # 1. Idempotency: oldin bunday key bilan transaction bormi?
    res = await db.execute(
        select(BalanceTransaction)
        .where(BalanceTransaction.idempotency_key == idempotency_key)
    )
    existing = res.scalar_one_or_none()
    user = await db.get(User, user_id)

    if not user:
        return None
    if existing:
        await db.refresh(user)
        return user

    # 2. Balansni oshirish
    user.balance = (user.balance or Decimal("0.00")) + amount

    # 3. Yozib qo‘yish
    txn = BalanceTransaction(
        user_id=user_id,
        booking_id=None,
        type=TransactionType.TOPUP,
        amount=amount,
        idempotency_key=idempotency_key
    )
    db.add(txn)

    await db.commit()
    await db.refresh(user)
    return user