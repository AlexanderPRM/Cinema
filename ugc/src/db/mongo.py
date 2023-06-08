from typing import Optional

import backoff
from core.config import project_settings
from motor import motor_asyncio
from pymongo.errors import ExecutionTimeout, NetworkTimeout, WaitQueueTimeoutError


class Mongo:
    def __init__(self, uri) -> None:
        self.client = motor_asyncio.AsyncIOMotorClient(host=uri)
        self.database = self.client[project_settings.MONGO_DB]

    @backoff.on_exception(
        backoff.expo,
        (NetworkTimeout, ExecutionTimeout, WaitQueueTimeoutError),
        max_time=20,
        max_tries=5,
    )
    def get_collection(self, collection):
        return self.database[collection]

    @backoff.on_exception(
        backoff.expo,
        (NetworkTimeout, ExecutionTimeout, WaitQueueTimeoutError),
        max_time=20,
        max_tries=5,
    )
    def call_mongo_collection_function(self, collection, function, **kwargs):
        return getattr(self.database[collection], function)(kwargs)


mongo: Optional[Mongo] = None


def get_db() -> Mongo:
    return mongo
