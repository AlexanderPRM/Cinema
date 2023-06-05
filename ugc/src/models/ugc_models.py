from datetime import datetime
from typing import Optional
from uuid import UUID

from models.base import OrjsonBaseModel


class Bookmark(OrjsonBaseModel):
    user_id: str
    film_id: str
    created_at: Optional[datetime] = None


class FilmReview(OrjsonBaseModel):
    text: str


class Review(OrjsonBaseModel):
    id: str
    film_id: UUID
    author: UUID
    text: str
    created_at: str
