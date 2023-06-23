from uuid import uuid4

import asyncpg
import backoff
from asyncpg.exceptions import CannotConnectNowError, TooManyConnectionsError
from core.config import postgres_settings


class PostgreSQL:
    def __init__(self, connection) -> None:
        self.connection: asyncpg.connection = connection

    @backoff.on_exception(
        backoff.expo, (TooManyConnectionsError, CannotConnectNowError), max_tries=5, max_time=10
    )
    async def get_user(self, user_id):
        return await self.connection.fetch(
            "SELECT * FROM %s WHERE user_id = '%s'"
            % (postgres_settings.POSTGRES_SUBSCRIBE_TABLE, user_id)
        )

    @backoff.on_exception(
        backoff.expo, (TooManyConnectionsError, CannotConnectNowError), max_tries=5, max_time=10
    )
    async def unsubscribe_user(self, user_id):
        return await self.connection.fetch(
            "INSERT INTO %s VALUES ('%s', '%s')"
            % (postgres_settings.POSTGRES_SUBSCRIBE_TABLE, uuid4(), user_id)
        )

    @backoff.on_exception(
        backoff.expo, (TooManyConnectionsError, CannotConnectNowError), max_tries=5, max_time=10
    )
    async def return_subscribe_for_user(self, user_id):
        return await self.connection.fetch(
            "DELETE FROM %s WHERE user_id = '%s'"
            % (postgres_settings.POSTGRES_SUBSCRIBE_TABLE, user_id)
        )


async def get_db():
    return PostgreSQL(
        await asyncpg.connect(
            user=postgres_settings.NOTF_POSTGRES_USER,
            password=postgres_settings.NOTF_POSTGRES_PASSWORD,
            host=postgres_settings.NOTF_POSTGRES_HOST,
            port=postgres_settings.NOTF_POSTGRES_PORT,
            database=postgres_settings.NOTF_POSTGRES_DB,
        )
    )
