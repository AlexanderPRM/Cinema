from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Entry(BaseModel):
    movie_id: UUID
    user_id: UUID
    updated_at: datetime
    timestamp: str

    class Config:
        validate_all = True
