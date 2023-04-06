from abc import abstractmethod
from typing import Any


class BaseCache:
    CACHE_EXPIRE_IN_SECONDS = 300

    @abstractmethod
    async def get_object_from_cache(self, url: str):
        pass

    @abstractmethod
    async def put_object_to_cache(self, url: str, data: Any):
        pass
