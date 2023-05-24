import logging

import uvicorn
from api.v1 import films, genres, persons
from core.config import config
from core.logger import LOGGING
from db import elastic, redis_db
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

app = FastAPI(
    title=config.PROJECT_NAME,
    description="Информация о фильмах, жанрах и людях, участвовавших в создании произведения",
    version=config.PROJECT_VERSION,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    # Подключаемся к базам при старте сервера
    # Подключиться можем при работающем event-loop
    # Поэтому логика подключения происходит в асинхронной функции
    redis_db.redis = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
    elastic.es = AsyncElasticsearch(hosts=[f"{config.ELASTIC_HOST}:{config.ELASTIC_PORT}"])


@app.on_event("shutdown")
async def shutdown():
    # Отключаемся от баз при выключении сервера
    await redis_db.redis.close()
    await elastic.es.close()


# Подключаем роутер к серверу, указав префикс /v1/films
# Теги указываем для удобства навигации по документации
app.include_router(films.router, prefix="/api/v1/films", tags=["Фильмы"])
app.include_router(genres.router, prefix="/api/v1/genres", tags=["Жанры"])
app.include_router(persons.router, prefix="/api/v1/persons", tags=["Персонажи"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
