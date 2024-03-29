import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseModelOrjson(BaseModel):
    id: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Film(BaseModelOrjson):
    title: str
    imdb_rating: float


class FilmDetail(BaseModelOrjson):
    title: str
    imdb_rating: float
    description: str | None
    genre: list[dict | None]
    actors: list[dict | None]
    writers: list[dict | None]
    director: list[str | None]


class Genre(BaseModelOrjson):
    name: str


class Person(BaseModelOrjson):
    full_name: str
    films: list[dict]


class PersonList(BaseModelOrjson):
    full_name: str
