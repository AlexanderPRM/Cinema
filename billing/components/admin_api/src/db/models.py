import datetime
import uuid

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class SubscriptionsTiers(Base):
    __tablename__ = "subscriptions_tiers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    cost = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    discount = Column(Integer, default=0, nullable=False)
    discount_duratation = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.now)
    updated_at = Column(
        DateTime(timezone=True), default=datetime.datetime.now, onupdate=datetime.datetime.now
    )
