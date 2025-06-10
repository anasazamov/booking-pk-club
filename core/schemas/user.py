from pydantic import BaseModel

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

    class Config:
        orm_mode = True
