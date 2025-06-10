from pydantic import BaseModel, Field
from decimal import Decimal
from core.schemas.user import UserRead

class BalanceRead(UserRead):
    pass

class TopUpRequest(BaseModel):
    user_id: int = Field(..., ge=1, example=1)
    amount: Decimal = Field(..., example="50.00")

class TopUpResponse(UserRead):
    pass