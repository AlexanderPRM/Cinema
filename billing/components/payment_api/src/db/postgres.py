import datetime
import time
import uuid

import backoff
from asyncpg.exceptions import CannotConnectNowError, TooManyConnectionsError
from core.config import postgres_settings
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


class PostgreSQL:
    def __init__(self, conn_url, **kwargs) -> None:
        self.engine = create_async_engine(conn_url, **kwargs)
        self.session: AsyncSession = async_sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )

    @backoff.on_exception(
        backoff.expo, (TooManyConnectionsError, CannotConnectNowError), max_tries=5, max_time=10
    )
    async def get_object_by_id(self, object_name: str, id: str):
        if object_name == postgres_settings.TRANSACTIONS_LOG_TABLE:
            id_name = "transaction_id"
        else:
            id_name = "id"
        async with self.session() as session:
            async with session.begin():
                resp = await session.execute(
                    text("SELECT * FROM %s WHERE %s = '%s'" % (object_name, id_name, id))
                )
            return resp.one_or_none()

    @backoff.on_exception(
        backoff.expo, (TooManyConnectionsError, CannotConnectNowError), max_tries=5, max_time=10
    )
    async def get_subscription_by_user_id(self, user_id: str):
        async with self.session() as session:
            async with session.begin():
                resp = await session.execute(
                    text("SELECT * FROM subscriptions WHERE user_id = '%s'" % (user_id))
                )
            return resp.one_or_none()

    @backoff.on_exception(
        backoff.expo, (TooManyConnectionsError, CannotConnectNowError), max_tries=5, max_time=10
    )
    async def get_transaction_by_user_id(self, id: str):
        async with self.session() as session:
            async with session.begin():
                resp = await session.execute(
                    text(
                        "SELECT * FROM %s WHERE user_id = '%s' ORDER BY created_at DESC LIMIT 1"
                        % (postgres_settings.TRANSACTIONS_LOG_TABLE, id)
                    )
                )
            return resp.all()

    @backoff.on_exception(
        backoff.expo, (TooManyConnectionsError, CannotConnectNowError), max_tries=5, max_time=10
    )
    async def update_transaction_status_to_canceled(self, transaction_id):
        async with self.session() as session:
            async with session.begin():
                resp = await session.execute(
                    text(
                        "UPDATE %s SET operate_status = 'canceled' WHERE transaction_id = '%s'"
                        % (postgres_settings.TRANSACTIONS_LOG_TABLE, transaction_id)
                    )
                )
            return resp

    @backoff.on_exception(
        backoff.expo, (TooManyConnectionsError, CannotConnectNowError), max_tries=5, max_time=10
    )
    async def update_transaction_status_to_success(self, transaction_id):
        async with self.session() as session:
            async with session.begin():
                resp = await session.execute(
                    text(
                        "UPDATE %s SET operate_status = 'success' WHERE transaction_id = '%s'"
                        % (postgres_settings.TRANSACTIONS_LOG_TABLE, transaction_id)
                    )
                )
            return resp

    @backoff.on_exception(
        backoff.expo, (TooManyConnectionsError, CannotConnectNowError), max_tries=5, max_time=10
    )
    async def create_subscription(self, transaction, payment_details, subscription_tiers):
        async with self.session() as session:
            async with session.begin():
                query = """
                    INSERT INTO subscriptions (id, user_id, transaction_id, subscription_tier_id,
                    ttl, auto_renewal, created_at, updated_at)
                    VALUES ('{id}', '{user_id}', '{transaction_id}', '{subscription_tier_id}',
                    {ttl}, {auto_renewal}, '{created_at}', '{updated_at}')
                """.format(
                    id=uuid.uuid4(),
                    user_id=transaction.user_id,
                    transaction_id=transaction.id,
                    subscription_tier_id=payment_details["subscribe_tier_id"],
                    ttl=int(time.time()) + subscription_tiers.duration,
                    auto_renewal=payment_details["auto_renewal"],
                    created_at=datetime.datetime.now(),
                    updated_at=datetime.datetime.now(),
                )
                await session.execute(text(query))

    @backoff.on_exception(
        backoff.expo, (TooManyConnectionsError, CannotConnectNowError), max_tries=5, max_time=10
    )
    async def update_subscription(self, transaction, payment_details, subscription_tiers):
        async with self.session() as session:
            async with session.begin():
                query = """
                    UPDATE subscriptions
                    SET transaction_id = '{transaction_id}',
                        subscription_tier_id = '{subscription_tier_id}',
                        ttl = {ttl}
                    WHERE user_id = '{user_id}'
                """.format(
                    transaction_id=transaction.id,
                    subscription_tier_id=payment_details["subscribe_tier_id"],
                    ttl=int(time.time()) + subscription_tiers.duration,
                    user_id=transaction.user_id,
                )
                await session.execute(text(query))

    @backoff.on_exception(
        backoff.expo, (TooManyConnectionsError, CannotConnectNowError), max_tries=5, max_time=10
    )
    async def deactivate_subscribe(self, user_id):
        async with self.session() as session:
            async with session.begin():
                subscription = await session.execute(
                    text(
                        "SELECT * FROM %s WHERE user_id = '%s'"
                        % (postgres_settings.SUBSCRIPTIONS_USERS_TABLE, user_id)
                    )
                )
                subscription = subscription.one()
                if subscription.ttl <= int(time.time()) and subscription.auto_renewal is False:
                    return
                await session.execute(
                    text(
                        "UPDATE %s SET ttl = $1, auto_renewal = $2 WHERE user_id = $3"
                        % (postgres_settings.SUBSCRIPTIONS_USERS_TABLE),
                        int(time.time()),
                        False,
                        user_id,
                    )
                )


async def get_db() -> PostgreSQL:
    return PostgreSQL(postgres_settings.POSTGRESQL_URL)
