import os

from dotenv import load_dotenv
from redis import Redis, StrictRedis

load_dotenv()


async def get_redis() -> Redis:
    con = StrictRedis(host=os.environ.get("REDIS_HOST"), port=os.environ.get("REDIS_PORT"), db=0)
    return con
