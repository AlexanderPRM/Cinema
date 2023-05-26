from typing import Optional

from redis.asyncio import Redis

redis: Optional[Redis] = None


def get_redis() -> Redis:
    return redis
