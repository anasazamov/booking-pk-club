from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas.otp import OTPRequest, OTPVerify, OTPOut
from core.crud.otp import create_otp, verify_otp
from core.services.otp import send_otp_via_eskiz
from core.database.db_helper import db_helper
from core.tasks.cleanup import send_otp

router = APIRouter(prefix="/auth", tags=["auth"])
get_db = db_helper.scoped_session_dependency

@router.post("/otp", status_code=status.HTTP_204_NO_CONTENT)
async def request_otp(
    data: OTPRequest,
    db: AsyncSession = Depends(get_db),
):

    try:
        code = await create_otp(db, data.phone_number)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    send_otp.delay(data.phone_number, code)
    return {"message": "OTP sent successfully"}

@router.post("/verify", response_model=OTPOut)
async def verify(
    data: OTPVerify,
    db: AsyncSession = Depends(get_db),
):

    valid = await verify_otp(db, data.phone_number, data.code)
    if not valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )
    return OTPOut(phone_number=data.phone_number, verified=True).model_dump()