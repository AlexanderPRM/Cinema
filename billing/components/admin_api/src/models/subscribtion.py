from pydantic import BaseModel


class Subscribtion(BaseModel):
    title: str
    duration: int
    cost: int
    description: str
    discount: int = 0
    discount_duratation: str | None = None
