import logging

import uvicorn
from api.v1 import film_view
from core.config import config
from db import redis_db
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

app = FastAPI(
    title=config.UGC_PROJECT_NAME,
    description="Отслеживание прогресса просмотра фильма",
    version=config.UGC_PROJECT_VERSION,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    redis_db.redis = Redis(host=config.UGC_REDIS_HOST, port=config.UGC_REDIS_PORT)


@app.on_event("shutdown")
async def shutdown():
    await redis_db.redis.close()


app.include_router(
    film_view.router,
    prefix="/api/v1/films/watch",
    tags=["Отслеживание просмотра фильмов пользователями"],
)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8001, log_level=logging.DEBUG)
