import random
import string
from datetime import datetime, timedelta
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.models.models import OTP, User
from core.config import settings

async def create_otp(db: AsyncSession, phone_number: str) -> str:

    result = await db.execute(select(User).where(User.phone_number == phone_number))
    user = result.scalar_one_or_none()
    if not user:
        raise ValueError("User not found")
    
    code = ''.join(random.choices(string.digits, k=6))
    now = datetime.utcnow()
    expires_at = now + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)
    otp = OTP(user_id=user.id, code=code, created_at=now, expires_at=expires_at)
    db.add(otp)
    await db.commit()
    return code

async def verify_otp(db: AsyncSession, phone_number: str, code: str) -> bool:
  
    result = await db.execute(select(User).where(User.phone_number == phone_number))
    user = result.scalar_one_or_none()
    if not user:
        return False
   
    q = await db.execute(
        select(OTP)
        .where(
            OTP.user_id == user.id,
            OTP.code == code,
            OTP.expires_at > datetime.utcnow()
        )
        .order_by(OTP.created_at.desc())
    )
    otp = q.scalar_one_or_none()
    if not otp:
        return False
 
    user.is_verified = True
  
    await db.execute(
        OTP.__table__.delete().where(OTP.user_id == user.id)
    )
    await db.commit()
    return True