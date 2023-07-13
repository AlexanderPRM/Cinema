import datetime
import uuid

from sqlalchemy import Column, DateTime, Enum, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Subscriptions(Base):
    __tablename__ = "subscriptions_tiers"
    title = Column(String, nullable=False)
    subscribe_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    duratation = Column(DateTime, nullable=False)
    cost = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    discount = Column(Integer, default=0, nullable=False)
    discount_duratation = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.now)
    updated_at = Column(
        DateTime(timezone=True), default=datetime.datetime.now, onupdate=datetime.datetime.now
    )


class SubscriptionsUsers(Base):
    __tablename__ = "subscriptions"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transaction_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subscribe_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ttl = Column(DateTime, nullable=False)
    auto_renewal = Column(Boolean, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.now)
    updated_at = Column(
        DateTime(timezone=True), default=datetime.datetime.now, onupdate=datetime.datetime.now
    )


class TransactionsLog(Base):
    __tablename__ = "transactions_log"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transaction_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    value = Column(Integer, nullable=False)
    provider = Column(String, nullable=False)
    idempotency_key_ttl = Column(DateTime, nullable=False)
    idempotency_key = Column(UUID(as_uuid=True), nullable=False)
    StatusEnum = ENUM('SUCCESS', 'ERROR', 'WAITING', name='status_enum')
    operate_status = Column(StatusEnum, default='WAITING', nullable=False)
    payment_details = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.now)
    updated_at = Column(
        DateTime(timezone=True), default=datetime.datetime.now, onupdate=datetime.datetime.now
    )
