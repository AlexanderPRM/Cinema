from redis import Redis

from core.config import config
from db.kafka_db import init_kafka
from db.clickhouse_db import init_clickhouse
from utils.state import State
from etl_classes.extract import Extract
from etl_classes.transform import Transform
from etl_classes.load import Loader



def run_etl():
    kafka = init_kafka()
    clickhouse = init_clickhouse()
    storage = State(
        Redis(host=config.UGC_ETL_REDIS_HOST, port=config.UGC_ETL_REDIS_PORT, db=0)
    )
    exctractor = Extract(kafka, 100, storage)
    exctractor.gen_data()
    transformer = Transform()
    loader = Loader(clickhouse)
    for entries in exctractor.extract():
        entries_to_save = transformer.transform(entries)
        loader.load_data_to_ch(entries_to_save)


if __name__ == "__main__":
    run_etl()
