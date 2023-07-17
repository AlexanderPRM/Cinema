import datetime
import enum
import uuid

from sqlalchemy import Column, DateTime, Enum, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class OperateStatus(enum.Enum):
    waiting = "WAITING"
    success = "SUCCESS"
    error = "ERROR"
    canceled = "CANCELED"


class Transactions(Base):
    __tablename__ = "transactions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    transaction_id = Column(UUID(as_uuid=True), nullable=False)
    value = Column(Integer, nullable=False)
    currency = Column(String, nullable=False)
    provider = Column(String, nullable=False)
    idempotency_key = Column(UUID(as_uuid=True), nullable=False, unique=True)
    operate_status = Column(Enum(OperateStatus), default=OperateStatus.waiting, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.now)
    updated_at = Column(
        DateTime(timezone=True), default=datetime.datetime.now, onupdate=datetime.datetime.now
    )
