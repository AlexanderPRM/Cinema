import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class Transaction(BaseModel):
    user_id: uuid.UUID
    transaction_id: uuid.UUID
    value: int
    provider: str
    currency: str
    idempotency_key: uuid.UUID
    operate_status: Literal["success", "error", "waiting", "canceled"]
    payment_details: dict
    created_at: datetime
    updated_at: datetime
