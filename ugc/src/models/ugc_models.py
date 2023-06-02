from datetime import datetime
from typing import Optional

from base import OrjsonBaseModel


class Bookmark(OrjsonBaseModel):
    user_id: str
    film_id: str
    created_at: Optional[datetime] = None


class FilmReview(OrjsonBaseModel):
    text: str
