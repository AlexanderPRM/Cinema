import os
from time import sleep

import elasticsearch
import psycopg2
from app.elastic_load import ElasticLoad
from app.postgres_extractor import PostgtresExtractor
from app.transform import TransformToElasticView
from dotenv import load_dotenv
from utils import backoff, state

load_dotenv("config.env")

JSON_FILEPATH = "etl/state.json"
INDEX = "movies"


ELASTIC_HOST = os.getenv("ELASTIC_HOST", default="127.0.0.1")
ELASTIC_PORT = os.getenv("ELASTIC_PORT", default="9200")
ELASTIC_ADRESS = f"http://{ELASTIC_HOST}:{ELASTIC_PORT}/"

TIME_TO_SLEEP = os.getenv("TIME_TO_SLEEP", default=300)
DB_NAME = os.getenv("POSTGRES_DB", default="postgres")
DB_PORT = os.getenv("POSTGRES_PORT", default="5432")
DB_HOST = os.getenv("POSTGRES_HOST", default="127.0.0.1")
DB_USER = os.getenv("POSTGRES_USER", default="postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", default="postgres")

DSN = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


@backoff.backoff()
def connect_to_psql(dsn: str):
    conn = psycopg2.connect(dsn=dsn)
    return conn


@backoff.backoff()
def connect_to_elastic(adress: str):
    conn = elasticsearch.Elasticsearch(adress)
    return conn


if __name__ == "__main__":
    psql_conn, elastic_conn = connect_to_psql(DSN), connect_to_elastic(ELASTIC_ADRESS)

    storage = state.State(state.JsonFileStorage(JSON_FILEPATH))
    psql = PostgtresExtractor(conn=psql_conn, storage=storage, limit=100)
    transformer = TransformToElasticView(INDEX)
    elastic = ElasticLoad(elastic_conn, INDEX)
    while True:
        while data := psql.extract():
            transform_data = transformer.transform(data)
            elastic.load(transform_data)
        sleep(TIME_TO_SLEEP)
    psql_conn.close()
    elastic_conn.transport.close()
