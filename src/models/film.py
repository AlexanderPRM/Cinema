import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseModelOrjson(BaseModel):
    json_loads = orjson.loads
    json_dumps = orjson_dumps


class Film(BaseModelOrjson):
    id: str
    title: str
    imdb_rating: float


class FilmDetail(BaseModelOrjson):
    id: str
    title: str
    imdb_rating: float
    desription: str | None
    genre: list[dict | None]
    actors: list[dict | None]
    writers: list[dict | None]
    director: list[str | None]


class Genre(BaseModelOrjson):
    id: str
    name: str


class Person(BaseModelOrjson):
    id: str
    full_name: str
    films: list[dict]


class PersonList(BaseModelOrjson):
    id: str
    full_name: str


# Не нашли применения для данных моделей, но
# согласно ТЗ, они должны быть.
class Actor(BaseModelOrjson):
    id: str
    full_name: str
    films: list[str]


class Director(BaseModelOrjson):
    id: str
    full_name: str
    films: list[str]


class Writer(BaseModelOrjson):
    id: str
    full_name: str
    films: list[str]
