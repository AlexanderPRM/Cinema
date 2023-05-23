import logging

import redis
import uvicorn
from api.v1 import film_view
from db import redis_db
from core.config import config, kafka_config
from db.kafka_db import Kafka, init_kafka
from etl.extract import Extract
from etl.transform import Transform
from etl.utils.state import State
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis import Redis

app = FastAPI(
    title=config.UGC_PROJECT_NAME,
    description="Отслеживание прогресса просмотра фильма",
    version=config.UGC_PROJECT_VERSION,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)

#вынести в отдельный контейнер
def run_etl():
    kafka = init_kafka()
    storage = State(
        redis.Redis(host=config.UGC_ETL_REDIS_HOST, port=config.UGC_ETL_REDIS_PORT, db=0)
    )
    exctractor = Extract(kafka, 100, storage)
    exctractor.gen_data()
    transformer = Transform()
    for entries in exctractor.extract():
        entries_to_save = transformer.transform(entries)
        for entry_to_save in entries_to_save:
            print(entry_to_save)
            #запись в клик


@app.on_event("startup")
async def startup():
    redis_db.redis = Redis(host=config.UGC_REDIS_HOST, port=config.UGC_REDIS_PORT)


app.include_router(
    film_view.router,
    prefix="/api/v1/films/watch",
    tags=["Отслеживание просмотра фильмов пользователями"],
)


if __name__ == "__main__":
    run_etl()
    uvicorn.run("main:app", port=8001, log_level=logging.DEBUG)
