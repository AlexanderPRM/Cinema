import datetime
import logging
from typing import Optional

import jwt
from core.config import config
from db.kafka_db import Kafka, init_kafka
from db.redis_db import get_redis
from fastapi import APIRouter, Cookie, Depends
from redis.asyncio import Redis

router = APIRouter()


@router.post("/{film_id}", status_code=201)
async def film_watch(
    film_id: str,
    access_token_cookie: Optional[str] = Cookie(),
    redis: Redis = Depends(get_redis),
    kafka: Kafka = Depends(init_kafka),
):
    try:
        payload = jwt.decode(access_token_cookie, config.JWT_SECRET, algorithms=["HS256"])
    except (jwt.exceptions.ExpiredSignatureError, jwt.exceptions.DecodeError) as err:
        logging.error(err)
        return {"message": "Token invalid"}

    key = str(payload["user_id"] + film_id)
    film_time = str(datetime.datetime.now())

    await kafka.save_entry("users_films", film_time, key)
    await redis.setex(key, value=film_time, time=int(config.FILM_WATCH_TIME_EXPIRED))
    return {"message": "OK", "timestamp": film_time}


@router.get("/{film_id}", status_code=200)
async def get_timestamp(
    film_id: str, access_token_cookie: Optional[str] = Cookie(), redis: Redis = Depends(get_redis)
):
    try:
        payload = jwt.decode(access_token_cookie, config.JWT_SECRET, algorithms=["HS256"])
    except (jwt.exceptions.ExpiredSignatureError, jwt.exceptions.DecodeError) as err:
        logging.error(err)
        return {"message": "Token invalid"}

    key = str(payload["user_id"] + film_id)
    timestamp = await redis.get(key)
    if timestamp:
        timestamp = timestamp.decode("utf-8")
    return {"message": "OK", "timestamp": timestamp}
