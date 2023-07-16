from typing import Any

from pydantic import BaseModel


class Subscribtion(BaseModel):
    subscribe_id: Any = None
    title: str
    duratation: int
    cost: int
    description: str
    discount: int = 0
    discount_duratation: str | None = None
