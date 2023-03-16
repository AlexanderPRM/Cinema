from typing import List

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class Film(BaseModel):
    id: str
    title: str
    imdb_rating: float
    description: str
    genre: list[dict]
    actors: list[dict]
    writers: list[dict]
    director: list

    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Genre(BaseModel):
    id: str
    name: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Person(BaseModel):
    id: str
    full_name: str
    films: list[dict]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class PersonList(BaseModel):
    id: str
    full_name: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


# Не нашли применения для данных моделей, но
# согласно ТЗ, они должны быть.
class Actor(BaseModel):
    id: str
    full_name: str
    films: List[str]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Director(BaseModel):
    id: str
    full_name: str
    films: List[str]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Writer(BaseModel):
    id: str
    full_name: str
    films: List[str]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
