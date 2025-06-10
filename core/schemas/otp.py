from pydantic import BaseModel, Field

class OTPRequest(BaseModel):
    phone_number: str = Field(..., example="+998901234567")
    chat_id: int = Field(..., example=123456789)

class OTPVerify(BaseModel):
    phone_number: str = Field(..., example="+998901234567")
    code: str = Field(..., min_length=6, max_length=6, example="123456")

class OTPOut(BaseModel):
    phone_number: str
    verified: bool