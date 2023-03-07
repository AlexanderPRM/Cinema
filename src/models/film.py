import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class ConfigMixin(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Film(BaseModel, ConfigMixin):
    id: str
    title: str
    description: str


class Genres(BaseModel, ConfigMixin):
    id: str
    name: str
    description: str


class Actors(BaseModel, ConfigMixin):
    id: str
    full_name: str


class Writers(BaseModel, ConfigMixin):
    id: str
    full_name: str


class Directors(BaseModel, ConfigMixin):
    id: str
    full_name: str
