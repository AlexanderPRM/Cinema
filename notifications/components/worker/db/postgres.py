import asyncpg
import backoff
from asyncpg.exceptions import CannotConnectNowError, TooManyConnectionsError
from core.config import postgres_settings


class PostgreSQLConsumer:
    def __init__(self, connection) -> None:
        self.connection: asyncpg.connection = connection

    @backoff.on_exception(
        backoff.expo, (TooManyConnectionsError, CannotConnectNowError), max_tries=5, max_time=10
    )
    async def get_template(self, template_id):
        return await self.connection.fetch(
            "SELECT * FROM %s WHERE id = '%s'" % (postgres_settings.TEMPLATE_TABLE, template_id)
        )

    @backoff.on_exception(
        backoff.expo, (TooManyConnectionsError, CannotConnectNowError), max_tries=5, max_time=10
    )
    async def get_subscribe_user(self, user_id):
        return await self.connection.fetch(
            "SELECT * FROM %s WHERE user_id = '%s'"
            % (postgres_settings.POSTGRES_SUBSCRIBE_TABLE, user_id)
        )
