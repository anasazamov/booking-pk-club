from pydantic import BaseModel
from datetime import datetime as da

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    password: str

class UserRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone_number: str
    is_active: bool
    role: str
    balance: float | None = 0.0
    created_at: da
    updated_at: da | None = None
    is_verified: bool = False

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    role: str | None = None
    is_active: bool | None = True

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        use_enum_values = True