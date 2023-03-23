from typing import Any, Optional
from cache.base import BaseCache
import json

from db.redis_db import Redis

class RedisCache(BaseCache):

    def __init__(self, redis: Redis, expire: int = None):
        self.redis = redis
        self.expire = expire or self.CACHE_EXPIRE_IN_SECONDS

    async def get_object_from_cache(self, url: str) -> Optional[Any]:
        result = await self.redis.get(str(url),)
        if result:
            result = json.loads(result)
        return result

    async def put_object_to_cache(self, url: str, data: Any):
        data = json.dumps(data)
        # setex позволяет time expire сделать
        await self.redis.setex(name=str(url), value=data, time=self.expire)
