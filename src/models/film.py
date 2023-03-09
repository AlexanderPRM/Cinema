import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


class Film(BaseModel):
    id: str
    title: str
    description: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Genres(BaseModel):
    id: str
    name: str
    description: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Actors(BaseModel):
    id: str
    full_name: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Writers(BaseModel):
    id: str
    full_name: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Directors(BaseModel):
    id: str
    full_name: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
