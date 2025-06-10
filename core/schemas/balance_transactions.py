# core/schemas/balance_transaction.py

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from decimal import Decimal
from typing import Optional

from core.schemas.booking import BookingRead
from core.database.models.models import TransactionType

class BalanceTransactionRead(BaseModel):
    id: int
    user_id: int
    booking_id: Optional[int]
    type: TransactionType
    amount: Decimal
    created_at: datetime

    booking: Optional[BookingRead]

    model_config = ConfigDict(from_attributes=True)
