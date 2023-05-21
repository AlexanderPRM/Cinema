from clickhouse_driver import Client
from core.config import ch_config
from db.base import BaseStorage


class ClickHouse(BaseStorage):
    def __init__(self, host, port) -> None:
        self.client = Client(host=host, port=port)

    def get_client(self):
        return self.client

    def get_entries():
        pass

    def save_entries(self):
        pass

    def save_entry():
        pass


def init_clickhouse():
    clickhouse = ClickHouse(host=ch_config.CLICKHOUSE_HOST, port=ch_config.CLICKHOUSE_PORT)
    return clickhouse
