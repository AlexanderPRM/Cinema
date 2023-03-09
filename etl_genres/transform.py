import json
import psycopg2
from psycopg2.extras import DictCursor
from psycopg2.extras import DictRow
from collections.abc import Generator  # используется для тайпингов
from typing import Tuple, Any
from functools import wraps
from pydantic import BaseModel
from typing import Optional


def coroutine(func):
    @wraps(func)
    def inner(*args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Generator:
        fn: Generator = func(*args, **kwargs)
        next(fn)
        return fn

    return inner


class TransformData_to_correct_json(BaseModel):
    id: str
    name: str = ""


@coroutine
def transform(batch: Generator) -> Generator[None, DictRow, None]:
    while data_list := (yield):
        json_body = ""
        for data in data_list:
            data_etl_json = dict(TransformData_to_correct_json(**dict(data)))

            index = {
                "index": {
                    "_index": "genres",
                    "_id": data_etl_json.get("id"),
                }
            }
            json_body += f"\n{json.dumps(index)}\n{json.dumps(data_etl_json)}\n"
        batch.send(json_body)
