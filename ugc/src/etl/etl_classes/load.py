import logging

from core.config import ch_config
from etl.utils.models import Entry


class Loader:
    def __init__(self, clickhouse):
        self.clickhouse = clickhouse

    def load_data_to_ch(self, data: list, ch_database="default", table_name=ch_config.CLICKHOUSE_TABLE_NAME, batch_size=1000):
        columns = ("user_id", "movie_id", "updated_at", "timestamp")
        query = "INSERT INTO {}.{} ({}) VALUES".format(ch_database, table_name, ', '.join(columns))
        values_list = list()
        for item in data:
            if not isinstance(item, Entry):
                logging.info(
                    "ClickHouse saving method get invalidated data: type={}, data={}".format(
                        type(item), item
                    )
                )
                continue
            values = "('{}','{}','{}', '{}')".format(
                str(item.user_id), str(item.movie_id), item.updated_at, str(item.timestamp)
            )
            values_list.append(values)
        batch_values = [values_list[i:i+batch_size] for i in range(0, len(values_list), batch_size)]
        self.clickhouse.save_entries(query, batch_values)
