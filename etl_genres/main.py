import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from backoff import backoff
from time import sleep
import psycopg2.extras
from config import settings
from contextlib import closing

from extract import load_from_postgres
from transform import transform
from load import load_to_etl


@backoff(start_sleep_time=0.1, factor=2, border_sleep_time=3)
def connect_to_database():
    dsl = {
        "dbname": settings.POSTGRES_DB,
        "user": settings.POSTGRES_USER,
        "password": settings.POSTGRES_PASSWORD,
        "host": settings.POSTGRES_HOST,
        "port": settings.POSTGRES_PORT,
    }
    with closing(psycopg2.connect(**dsl, cursor_factory=DictCursor)) as pg_conn:
        cursor_pg = pg_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            while True:
                tables = [
                    "content.genre",
                ]
                for table in tables:
                    unloads = load_to_etl()
                    multiplication = transform(unloads)
                    load_from_postgres(multiplication, cursor_pg, table)
                    sleep(5)

        finally:
            cursor_pg.close()
            pg_conn.close()


if __name__ == "__main__":
    connect_to_database()
