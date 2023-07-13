from typing import Optional

import asyncpg
from core.config import config, postgres_settings
from sqlalchemy.ext.asyncio import create_async_engine


class PostgreSQL:
    def __init__(self, conn_url, **kwargs) -> None:
        self.engine = create_async_engine(conn_url, **kwargs)
        self.conn = None

    async def get_transactions_list(self, page_size, page_number):
        offset = (page_number - 1) * page_size
        self.conn = await self.get_connection()
        query = f"SELECT * FROM {config.TRANSACTIONS_LOG_TABLE} LIMIT {page_size} OFFSET {offset}"
        result = await self.conn.fetch(query)
        return result

    async def get_connection(self):
        return await asyncpg.connect(
            user=postgres_settings.POSTGRES_USER,
            password=postgres_settings.POSTGRES_PASSWORD,
            database=postgres_settings.POSTGRES_DB,
            host=postgres_settings.POSTGRES_HOST,
        )


postgres_: Optional[PostgreSQL] = None


async def get_postgres() -> PostgreSQL:
    return postgres_
