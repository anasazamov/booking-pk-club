from fastapi import APIRouter, Depends
from core.api.deps import get_current_user
from core.database.db_helper import db_helper
from core.schemas.balance_transactions import BalanceTransactionRead
from sqlalchemy.ext.asyncio import AsyncSession
from core.database.models import User
from core.crud.balance_transaction import transactions_history
from typing import List

router = APIRouter(tags=['Transactions'], prefix='/transactions')

@router.get('/', response_model=List[BalanceTransactionRead])
async def get_transactions_history(
    db: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current: User = Depends(get_current_user)
):
    user_id = current.id
    return await transactions_history(user_id=user_id, db=db)