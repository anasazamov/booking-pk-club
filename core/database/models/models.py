from datetime import datetime, timedelta
from enum import Enum
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    ForeignKey,
    Numeric,
    Enum as SAEnum,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship, declarative_base
from core.database.models.base import Base

def now_plus(hours: int) -> datetime:
    return datetime.utcnow() + timedelta(hours=hours)


class RoleEnum(str, Enum):
    USER = "user"
    ADMIN = "admin"
    OWNER = "owner"


class User(Base):
    __tablename__ = "users"

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    role = Column(SAEnum(RoleEnum), default=RoleEnum.USER, nullable=False)
    balance = Column(Numeric(10, 2), default=0)

    # relationships
    otps = relationship("OTP", back_populates="user", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="user")
    balance_transactions = relationship("BalanceTransaction", back_populates="user")
    icafe_account = relationship("ICafeAccount", back_populates="user", uselist=False)


class OTP(Base):
    __tablename__ = "otps"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    code = Column(String(6), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, default=lambda: now_plus(5))  # 5 minutes validity

    user = relationship("User", back_populates="otps")


class Branch(Base):
    __tablename__ = "branches"

    name = Column(String(100), nullable=False)
    address = Column(String(200), nullable=True)

    zones = relationship("Zone", back_populates="branch")


class Zone(Base):
    __tablename__ = "zones"

    branch_id = Column(Integer, ForeignKey("branches.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)

    branch = relationship("Branch", back_populates="zones")
    places = relationship("Place", back_populates="zone")


class Place(Base):
    __tablename__ = "places"

    zone_id = Column(Integer, ForeignKey("zones.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(50), nullable=False)

    zone = relationship("Zone", back_populates="places")
    bookings = relationship("Booking", back_populates="place")


class BookingStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class Booking(Base):
    __tablename__ = "bookings"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    place_id = Column(Integer, ForeignKey("places.id", ondelete="CASCADE"), nullable=False)
    start_datetime = Column(DateTime, nullable=False, default=func.now())
    end_datetime = Column(DateTime, nullable=False)
    status = Column(SAEnum(BookingStatus), default=BookingStatus.PENDING, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # business rule: ensure no overlapping bookings at application level
    __table_args__ = (
        UniqueConstraint('place_id', 'start_datetime', 'end_datetime', name='uix_place_time'),
    )

    user = relationship("User", back_populates="bookings")
    place = relationship("Place", back_populates="bookings")
    balance_transactions = relationship("BalanceTransaction", back_populates="booking")
    icafe_booking = relationship("ICafeBooking", back_populates="booking", uselist=False)


class TransactionType(str, Enum):
    TOPUP = "topup"
    FREEZE = "freeze"
    RELEASE = "release"
    PAYMENT = "payment"


class BalanceTransaction(Base):
    __tablename__ = "balance_transactions"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    booking_id = Column(Integer, ForeignKey("bookings.id", ondelete="SET NULL"), nullable=True)
    type = Column(SAEnum(TransactionType), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="balance_transactions")
    booking = relationship("Booking", back_populates="balance_transactions")


class ICafeAccount(Base):
    __tablename__ = "icafe_accounts"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    external_user_id = Column(String(100), nullable=False, unique=True)
    synced_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="icafe_account")


class ICafeBooking(Base):
    __tablename__ = "icafe_bookings"

    booking_id = Column(Integer, ForeignKey("bookings.id", ondelete="CASCADE"), unique=True, nullable=False)
    external_booking_id = Column(String(100), nullable=False, unique=True)
    synced_at = Column(DateTime, default=func.now())

    booking = relationship("Booking", back_populates="icafe_booking")

# Note: Cleanup of unverified users older than 48 hours should be implemented via a scheduled Celery task.
