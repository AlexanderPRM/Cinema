from enum import Enum
from typing import List, Optional

from pydantic.main import BaseModel


class TypeEnum(str, Enum):
    new_episodes = "new_episodes"
    email_confirm = "email_confirm"
    recommendations = "recommendations"


class FilmData(BaseModel):
    film_id: str  # uuid
    film_name: str


class ListOfFilms(BaseModel):
    films_data: Optional[List[FilmData]]


class Context(BaseModel):
    users_id: Optional[List[str]] # Список uuid
    payload: Optional[ListOfFilms]
    link: Optional[str]


class Notification(BaseModel):
    type_send: TypeEnum = TypeEnum.new_episodes
    template_id: Optional[str] # Список uuid
    notification_id: Optional[str] # Список uuid
    context: Context
