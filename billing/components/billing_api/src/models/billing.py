from pydantic import BaseModel


class Pay(BaseModel):
    auto_renewal: bool
    idempotence_key: str
