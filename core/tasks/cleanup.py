from celery import Celery
from datetime import datetime, timedelta
from core.database.db_helper import db_helper
from core.database.models import User
from sqlalchemy import delete
from core.services.otp import send_otp_via_eskiz

celery = Celery(__name__)
celery.config_from_object('core.config', namespace='CELERY_')

@celery.on_after_configure.connect
async def setup_periodic_tasks(sender, **kwargs):
    # запускаем раз в день
    sender.add_periodic_task(24*3600, cleanup_unverified.s())

@celery.task
async def cleanup_unverified():
    async with db_helper.scoped_session_dependency() as db:
        cutoff = datetime.utcnow() - timedelta(hours=48)
        await db.execute(
            delete(User).where(User.is_verified == False, User.created_at < cutoff)
        )
        await db.commit()


@celery.task
async def send_otp(phone_number:str, code:str):
    await send_otp_via_eskiz(code, phone_number)

