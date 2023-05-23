from typing import Optional

from redis import Redis

redis: Optional[Redis] = None


def get_redis() -> Redis:
    return redis
