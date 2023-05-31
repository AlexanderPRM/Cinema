from uuid import UUID

from pydantic import BaseModel


class Review(BaseModel):
    id: str
    film_id: UUID
    author: UUID
    text: str
    created_at: str
