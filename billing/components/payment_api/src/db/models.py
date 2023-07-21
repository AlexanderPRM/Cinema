import datetime
import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Subscriptions(Base):
    __tablename__ = "subscriptions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, unique=True)
    transaction_id = Column(UUID(as_uuid=True), ForeignKey("transactions.id"), nullable=False)
    subscription_tier_id = Column(
        UUID(as_uuid=True), ForeignKey("subscriptions_tiers.id"), nullable=False
    )
    ttl = Column(Integer, nullable=False)
    auto_renewal = Column(Boolean, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.now)
    updated_at = Column(
        DateTime(timezone=True), default=datetime.datetime.now, onupdate=datetime.datetime.now
    )
