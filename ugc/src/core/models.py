from pydantic import BaseModel


class FilmReview(BaseModel):
    text: str
