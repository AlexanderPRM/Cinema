import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class Transaction(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    transaction_id: uuid.UUID
    value: int
    currency: str
    provider: str
    payment_details: dict
    idempotency_key: uuid.UUID
    operate_status: Literal["waiting", "success", "error", "canceled"]
    created_at: datetime
    updated_at: datetime
