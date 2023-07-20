import backoff
from asyncpg.exceptions import CannotConnectNowError, TooManyConnectionsError
from core.config import postgres_settings
import datetime


class PostgreSQLProducer:
    def __init__(self, connection):
        self.connection = connection

    async def __aenter__(self):
        await self.connection.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.connection.__aexit__(exc_type, exc_val, exc_tb)

    @backoff.on_exception(
        backoff.expo, (TooManyConnectionsError, CannotConnectNowError), max_tries=5, max_time=10
    )
    async def get_ended_subs(self, previous_run_time):
        query = (
            f"SELECT user_id, transaction_id, subscribe_id, ttl, auto_renewal, created_at, "
            f"updated_at FROM %s "
            f"WHERE ttl <= '%s' "
            f"AND ttl >= '%s' "
            f"GROUP BY transaction_id, user_id, subscribe_id ORDER BY ttl;" % (
                postgres_settings.SUBSCRIPTIONS_USERS_TABLE,
                datetime.datetime.now(),
                previous_run_time
            )
        )
        return await self.connection.fetch(query)

    async def get_subscriprion_cost(self, sub_id):
        query = (
            f"SELECT cost "
            f"FROM {postgres_settings.SUBSCRIPTIONS_TABLE} "
            f"WHERE subscribe_id = '{sub_id}' "
            f"FROM %s "
            f"WHERE subscribe_id = '%s' " % (
                postgres_settings.SUBSCRIPTIONS_TABLE,
                sub_id
            )
        )
        return await self.connection.fetch(query)

    async def get_transaction_currency(self, transaction_id):
        query = (
            f"SELECT currency "
            f"FROM %s "
            f"WHERE transaction_id = '%s' ORDER BY updated_at LIMIT 1" % (
                postgres_settings.TRANSACTIONS_LOG_TABLE,
                transaction_id
            )
        )
        return await self.connection.fetch(query)
