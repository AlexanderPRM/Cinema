from typing import List, Optional

from pydantic.main import BaseModel


class Film(BaseModel):
    id: str
    name: str


class Like(BaseModel):
    id: str


class FilmPayload(BaseModel):
    film_list: List[Film]


class LikePayload(BaseModel):
    liked_user_id: Like


class FilmContext(BaseModel):
    users_id: Optional[List[str]]
    payload: FilmPayload
    link: Optional[str]


class LikeContext(BaseModel):
    users_id: Optional[List[str]]
    payload: LikePayload
    link: Optional[str]


class FilmsNotification(BaseModel):
    template_id: Optional[str]
    type_send: str
    notification_id: str
    context: FilmContext
    category_name: Optional[str]


class LikesNotification(BaseModel):
    template_id: Optional[str]
    type_send: str
    notification_id: str
    context: LikeContext
    category_name: Optional[str]
