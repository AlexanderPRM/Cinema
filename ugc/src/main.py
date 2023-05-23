import logging

import redis
import uvicorn
from core.config import config, kafka_config
from db.kafka_db import Kafka
from db.clickhouse_db import init_clickhouse
from etl.extract import Extract
from etl.transform import Transform
from etl.load import Loader
from etl.utils.state import State
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title=config.UGC_PROJECT_NAME,
    description="Отслеживание прогресса просмотра фильма",
    version=config.UGC_PROJECT_VERSION,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


if __name__ == "__main__":
    kafka = Kafka(kafka_config.BOOTSTRAP_SERVERS)
    clickhouse = init_clickhouse()
    kafka.create_topics_with_partitions(12, "users_films")
    storage = State(
        redis.Redis(host=config.UGC_ETL_REDIS_HOST, port=config.UGC_ETL_REDIS_PORT, db=0)
    )
    exctractor = Extract(kafka, 100, storage)
    transformer = Transform()
    loader = Loader(clickhouse)
    exctractor.gen_data()
    for entries in exctractor.extract():
        entries_to_save = transformer.transform(entries)
        loader.load_data_to_ch(entries_to_save)
    print(clickhouse.get_entries())


    uvicorn.run("main:app", port=8001, log_level=logging.DEBUG)
