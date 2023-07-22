import time
from typing import Optional

import asyncpg
from core.config import postgres_settings
from sqlalchemy.ext.asyncio import create_async_engine


class PostgreSQL:
    def __init__(self, conn_url, **kwargs) -> None:
        self.engine = create_async_engine(conn_url, **kwargs)
        self.conn = None

    async def get_transactions_list(self, page_size, page_number):
        offset = (page_number - 1) * page_size
        self.conn = await self.get_connection()
        query = "SELECT * FROM %s LIMIT %s OFFSET %s" % (
            postgres_settings.TRANSACTIONS_LOG_TABLE,
            page_size,
            offset,
        )
        result = await self.conn.fetch(query)
        return result

    async def get_user_transactions_list(self, page_size, page_number, user_id):
        offset = (page_number - 1) * page_size
        self.conn = await self.get_connection()
        query = "SELECT * FROM %s WHERE user_id = '%s' LIMIT %s OFFSET %s" % (
            postgres_settings.TRANSACTIONS_LOG_TABLE,
            user_id,
            page_size,
            offset,
        )
        result = await self.conn.fetch(query)
        return result

    async def disable_auto_renewal(self, subscribe_id):
        self.conn = await self.get_connection()
        query = "UPDATE %s SET auto_renewal = False " "WHERE id = '%s' AND auto_renewal = True;" % (
            postgres_settings.SUBSCRIPTIONS_USERS_TABLE,
            subscribe_id,
        )
        await self.conn.execute(query)

    async def get_all_users_with_sub(self, subscribe_id):
        self.conn = await self.get_connection()
        query = (
            "SELECT user_id FROM %s "
            "WHERE id = '%s' AND ttl > '%s' "
            "AND auto_renewal = True;"
            % (postgres_settings.SUBSCRIPTIONS_USERS_TABLE, subscribe_id, int(time.time()))
        )

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
