from pydantic import BaseModel
from typing import Literal
import uuid
from datetime import datetime


class Transaction(BaseModel):
    user_id: uuid.UUID
    transaction_id: uuid.UUID
    value: int
    provider: str
    idempotency_key_ttl: datetime
    idempotency_key: uuid.UUID
    operate_status: Literal['SUCCESS', 'ERROR', 'WAITING']
    payment_details: str
    created_at: datetime
    updated_at: datetime

