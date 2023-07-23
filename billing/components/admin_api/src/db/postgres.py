import time
from typing import Optional

from core.config import postgres_settings
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


class PostgreSQL:
    def __init__(self, conn_url, **kwargs) -> None:
        self.engine = create_async_engine(conn_url, **kwargs)
        self.session: AsyncSession = async_sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )

    async def get_transactions_list(self, page_size, page_number):
        offset = (page_number - 1) * page_size
        async with self.session() as session:
            async with session.begin():
                query = "SELECT * FROM %s LIMIT %s OFFSET %s" % (
                    postgres_settings.TRANSACTIONS_LOG_TABLE,
                    page_size,
                    offset,
                )
                result = await session.execute(text(query))
            return result.all()

    async def get_user_transactions_list(self, page_size, page_number, user_id):
        offset = (page_number - 1) * page_size
        async with self.session() as session:
            async with session.begin():
                query = "SELECT * FROM %s WHERE user_id = '%s' LIMIT %s OFFSET %s" % (
                    postgres_settings.TRANSACTIONS_LOG_TABLE,
                    user_id,
                    page_size,
                    offset,
                )
                result = await session.execute(text(query))
            return result.all()

    async def disable_auto_renewal(self, subscribe_id):
        async with self.session as session:
            async with session.begin():
                query = (
                    "UPDATE %s SET auto_renewal = False "
                    "WHERE id = '%s' AND auto_renewal = True;"
                    % (
                        postgres_settings.SUBSCRIPTIONS_USERS_TABLE,
                        subscribe_id,
                    )
                )
                await session.execute(text(query))

    async def get_all_users_with_sub(self, subscribe_id):
        async with self.session() as session:
            async with session.begin():
                query = (
                    "SELECT user_id FROM %s "
                    "WHERE id = '%s' AND ttl > '%s' "
                    "AND auto_renewal = True;"
                    % (postgres_settings.SUBSCRIPTIONS_USERS_TABLE, subscribe_id, int(time.time()))
                )

                result = await self.conn.fetch(text(query))
            return result.all()


postgres_: Optional[PostgreSQL] = None


async def get_postgres() -> PostgreSQL:
    return postgres_
