from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from decimal import Decimal

class BookingStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"

class BookingBase(BaseModel):
    place_id: int = Field(..., ge=1)
    start_datetime: datetime = Field(...)
    end_datetime: datetime = Field(...)
    amount: Decimal = Field(..., example="10.00")

class BookingCreate(BookingBase):
    pass

class BookingRead(BookingBase):
    id: int
    user_id: int
    status: BookingStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class BookingUpdate(BaseModel):
    status: BookingStatus | None = None
    start_datetime: datetime | None = None
    end_datetime: datetime | None = None
    amount: Decimal | None = None