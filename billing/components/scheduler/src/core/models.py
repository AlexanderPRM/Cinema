import datetime
import uuid
from typing import List, Optional

from pydantic.main import BaseModel
from sqlalchemy import Column, DateTime, Enum, Integer, String
from sqlalchemy.dialects.postgresql import UUID
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


class Context(BaseModel):
    users_id: Optional[List[str]]
    payload: dict
    link: Optional[str]


class Notification(BaseModel):
    template_id: Optional[str]
    notification_id: Optional[str]
    context: Context
