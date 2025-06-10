from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from enum import Enum
from decimal import Decimal
from core.schemas.location import PlaceRead

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
    place_id: int

    model_config = ConfigDict(from_attributes=True)

class BookingUpdate(BaseModel):
    status: BookingStatus | None = None
    start_datetime: datetime | None = None
    end_datetime: datetime | None = None
    amount: Decimal | None = None