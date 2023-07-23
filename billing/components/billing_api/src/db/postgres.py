import time

from core.config import postgres_settings
from db.models import Transactions
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class PostgreSQL:
    def __init__(self, conn_url, **kwargs) -> None:
        self.engine: AsyncEngine = create_async_engine(conn_url, **kwargs)
        self.asyncsession: AsyncSession = async_sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )

    async def get_subscribe_tier(self, subscribe_tier_id):
        sql = "SELECT * FROM %s WHERE id = '%s'" % (
            postgres_settings.SUBSCRIPTIONS_TABLE,
            subscribe_tier_id,
        )
        async with self.asyncsession() as session:
            async with session.begin():
                res = await session.execute(text(sql))
            return res.one_or_none()

    async def insert_transaction(self, values: dict):
        async with self.asyncsession() as session:
            async with session.begin():
                insert_stmt = insert(Transactions).values(**values)
                do_nothing_on_conflict = insert_stmt.on_conflict_do_nothing(
                    index_elements=["idempotency_key"]
                )
                res = await session.execute(do_nothing_on_conflict)
            return res

    async def get_transaction_by_key(self, idempotency_key):
        async with self.asyncsession() as session:
            async with session.begin():
                sql = "SELECT * FROM %s WHERE idempotency_key = '%s'" % (
                    postgres_settings.TRANSACTIONS_LOG_TABLE,
                    idempotency_key,
                )
                res = await session.execute(text(sql))
            return res.one()

    async def get_transaction_by_id(self, idx):
        async with self.asyncsession() as session:
            async with session.begin():
                sql = "SELECT * FROM %s WHERE id = '%s'" % (
                    postgres_settings.TRANSACTIONS_LOG_TABLE,
                    idx,
                )
                res = await session.execute(text(sql))
            return res.one()

    async def get_subscibe_by_user(self, user_id):
        async with self.asyncsession() as session:
            async with session.begin():
                sql = "SELECT * FROM %s WHERE user_id = '%s'" % (
                    postgres_settings.SUBSCRIPTIONS_USERS_TABLE,
                    user_id,
                )
                res = await session.execute(text(sql))
            return res.one_or_none()

    async def update_auto_renewal_subscribe_by_user(self, user_id):
        async with self.asyncsession() as session:
            async with session.begin():
                sql = "UPDATE %s SET auto_renewal = FALSE WHERE user_id = '%s' RETURNING id" % (
                    postgres_settings.SUBSCRIPTIONS_USERS_TABLE,
                    user_id,
                )
                res = await session.execute(text(sql))
            return res.one()

    async def deactivate_subscribe(self, user_id):
        async with self.asyncsession() as session:
            async with session.begin():
                sql = (
                    "UPDATE %s SET auto_renewal = FALSE, ttl = %s WHERE user_id = '%s' RETURNING id"
                    % (
                        postgres_settings.SUBSCRIPTIONS_USERS_TABLE,
                        int(time.time()),
                        user_id,
                    )
                )
                res = await session.execute(text(sql))
            return res.one()


def get_db():
    return PostgreSQL(postgres_settings.POSTGRESQL_URL)
