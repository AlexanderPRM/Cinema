from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Movie(BaseModel):
    id: UUID
    title: str
    description: str | None
    rating: float | None
    type: str
    created_at: datetime
    updated_at: datetime
    persons: list[dict]
    genres: list[dict]

    class Config:
        validate_all = True
