from pydantic import BaseModel, Field


class Message(BaseModel):
    message: str


class Refund(BaseModel):
    idempotence_key: str


class Amount(BaseModel):
    value: float
    currency: str


class RefundResponse(BaseModel):
    status: str
    amount: Amount
    payment_id: str


class Pay(BaseModel):
    auto_renewal: bool
    currency: str = Field(default="RUB")
    idempotence_key: str


class Confirmation(BaseModel):
    confirmation_url: str
    type: str


class PayResponse(BaseModel):
    confirmation: Confirmation
    created_at: str


class UnsubscribeResponse(BaseModel):
    message: str
    subscribe_id: str
