import backoff
from clickhouse_driver import Client

from core.config import ch_config
from db.base import BaseStorage


class ClickHouse(BaseStorage):
    def __init__(self, host, port, node_1) -> None:
        self.client = Client(host=host, port=port)
        self.client_node_1 = Client(host=node_1)

    def get_client(self):
        return self.client

    @backoff.backoff(backoff.expo, max_time=30, max_tries=5)
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
        self.client_node_1.execute(query)

    @backoff.backoff(backoff.expo, max_time=30, max_tries=5)
    def get_entries(self, table_name: str = ch_config.CLICKHOUSE_TABLE_NAME, limit: int = 1000):
        query = "SELECT * FROM {} LIMIT {}".format(table_name, limit)
        client = self.get_client()
        result = client.execute(query)
        return result

    def save_entries(self, query: str, batch_values: list):
        client = self.get_client()
        for batch in batch_values:
            self.save_entry(query, batch, client)

    @backoff.backoff(backoff.expo, max_time=30, max_tries=5)
    def save_entry(self, query, batch, client: Client):
        query_full = query + ",".join(batch)
        client.execute(query_full)


def init_clickhouse():
    clickhouse = ClickHouse(
        host=ch_config.CLICKHOUSE_HOST,
        port=ch_config.CLICKHOUSE_PORT,
        node_1=ch_config.CLICKHOUSE_NODE_1
    )
    clickhouse.create_tables()
    return clickhouse
