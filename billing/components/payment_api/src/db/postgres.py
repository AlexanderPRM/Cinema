from typing import Optional

import asyncpg
import backoff
from asyncpg.exceptions import CannotConnectNowError, TooManyConnectionsError
from core.config import postgres_settings
from sqlalchemy.ext.asyncio import create_async_engine


class PostgreSQL:
    def __init__(self, conn_url, **kwargs) -> None:
        self.engine = create_async_engine(conn_url, **kwargs)
        self.conn = None
    
    @backoff.on_exception(
        backoff.expo, (TooManyConnectionsError, CannotConnectNowError), max_tries=5, max_time=10
    )
    async def get_transaction_by_payment_id(self, payment_id):
        self.conn = await self.get_connection()
        return await self.connection.fetch(
            "SELECT * FROM %s WHERE transaction_id = '%s'"
            % (postgres_settings.TRANSACTIONS_LOG_TABLE, payment_id)
        )

    @backoff.on_exception(
        backoff.expo, (TooManyConnectionsError, CannotConnectNowError), max_tries=5, max_time=10
    )
    async def update_transaction_status_to_error(self, transaction_id):
        self.conn = await self.get_connection()
        await self.connection.execute(
            "UPDATE %s SET operate_status = 'ERROR' WHERE transaction_id = '%s'"
            % (postgres_settings.TRANSACTIONS_LOG_TABLE, transaction_id)
        )

    @backoff.on_exception(
        backoff.expo, (TooManyConnectionsError, CannotConnectNowError), max_tries=5, max_time=10
    )
    async def update_transaction_status_to_success(self, transaction_id):
        self.conn = await self.get_connection()
        await self.connection.execute(
            "UPDATE %s SET operate_status = 'SUCCESS' WHERE transaction_id = '%s'"
            % (postgres_settings.TRANSACTIONS_LOG_TABLE, transaction_id)
        )

    # @backoff.on_exception(
    #     backoff.expo, (TooManyConnectionsError, CannotConnectNowError), max_tries=5, max_time=10
    # )
    # async def create_subscription(self, payment):
    #     self.conn = await self.get_connection()
    #     await self.connection.execute()

    async def get_connection(self):
        return await asyncpg.connect(
            user=postgres_settings.POSTGRES_USER,
            password=postgres_settings.POSTGRES_PASSWORD,
            database=postgres_settings.POSTGRES_DB,
            host=postgres_settings.POSTGRES_HOST,
        )


postgres: Optional[PostgreSQL] = None


async def get_db() -> PostgreSQL:
    return postgres