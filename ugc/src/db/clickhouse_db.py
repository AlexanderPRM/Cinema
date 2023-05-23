import logging

from clickhouse_driver import Client

from core.config import ch_config
from db.base import BaseStorage
from etl.utils.models import Entry


class ClickHouse(BaseStorage):
    def __init__(self, host, port) -> None:
        self.client = Client(host=host, port=port)

    def get_client(self):
        return self.client

    def create_tables(self):
        query = """
                CREATE TABLE IF NOT EXISTS users_films (
                user_id String,
                movie_id String,
                timestamp String,
                updated_at DateTime64
            ) ENGINE = MergeTree() PARTITION BY toYYYYMM(updated_at) ORDER BY (user_id, movie_id, timestamp)
        """
        client = self.get_client()
        client.execute(query)

    def get_entries(self, table_name=ch_config.CLICKHOUSE_TABLE_NAME, limit=1000):
        query = "SELECT * FROM {} LIMIT {}".format(table_name, limit)
        client = self.get_client()
        result = client.execute(query)
        return result

    def save_entries(self, query, batch_values):
        for batch in batch_values:
            self.save_entry(query, batch)

    def save_entry(self, query, batch):
        client = self.get_client()
        query_full = query + ','.join(batch)
        client.execute(query_full)


def init_clickhouse():
    clickhouse = ClickHouse(host=ch_config.CLICKHOUSE_HOST, port=ch_config.CLICKHOUSE_PORT)
    clickhouse.create_tables()
    return clickhouse
