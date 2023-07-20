import logging
import time

import backoff
from asyncpg.exceptions import CannotConnectNowError, TooManyConnectionsError
from core.config import postgres_settings


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
            "SELECT user_id, transaction_id, id, ttl, auto_renewal, created_at, "
            "updated_at FROM %s "
            "WHERE ttl <= '%s' "
            "AND ttl >= '%s' "
            "GROUP BY transaction_id, user_id, id ORDER BY ttl;"
            % (
                postgres_settings.SUBSCRIPTIONS_USERS_TABLE,
                int(time.time()),
                previous_run_time,
            )
        )
        logging.info(query)
        return await self.connection.fetch(query)

    async def get_subscriprion_cost(self, sub_id):
        query = (
            "SELECT cost "
            "FROM {postgres_settings.SUBSCRIPTIONS_TABLE} "
            "WHERE id = '{sub_id}' "
            "FROM %s "
            "WHERE id = '%s' " % (postgres_settings.SUBSCRIPTIONS_TABLE, sub_id)
        )
        return await self.connection.fetch(query)

    async def get_transaction_currency(self, transaction_id):
        query = (
            "SELECT currency "
            "FROM %s "
            "WHERE transaction_id = '%s' ORDER BY updated_at LIMIT 1"
            % (postgres_settings.TRANSACTIONS_LOG_TABLE, transaction_id)
        )
        return await self.connection.fetch(query)
