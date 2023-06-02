from datetime import datetime
from typing import Optional

import orjson as orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class OrjsonBaseModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Bookmark(OrjsonBaseModel):
    user_id: str
    film_id: str
    created_at: Optional[datetime] = None
