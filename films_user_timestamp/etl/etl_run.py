import asyncio

from core.config import config
from db.clickhouse_db import init_clickhouse
from db.kafka_db import init_kafka
from etl_classes.extract import Extract
from etl_classes.load import Loader
from etl_classes.transform import Transform
from redis import Redis
from utils.state import State


async def run_etl():
    kafka = await init_kafka()
    clickhouse = init_clickhouse()
    storage = State(Redis(host=config.UGC_ETL_REDIS_HOST, port=config.UGC_ETL_REDIS_PORT, db=0))
    exctractor = Extract(kafka, 100, storage)

    # Генерация тестовых данных
    # exctractor.gen_data()

    transformer = Transform()
    loader = Loader(clickhouse)
    async for entries in exctractor.extract():
        entries_to_save = transformer.transform(entries)
        loader.load_data_to_ch(entries_to_save)
        kafka.producer.flush()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_etl())
