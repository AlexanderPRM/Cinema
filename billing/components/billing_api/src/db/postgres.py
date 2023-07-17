from core.config import postgres_settings
from db.models import Transactions
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


class PostgreSQL:
    def __init__(self, conn_url, **kwargs) -> None:
        self.engine: AsyncEngine = create_async_engine(conn_url, **kwargs)
        self.asyncsession: AsyncSession = sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )

    async def get_subscribe_tier(self, subscribe_id):
        sql = "SELECT * FROM %s WHERE id = '%s'" % (
            postgres_settings.SUBSCRIPTIONS_TABLE,
            subscribe_id,
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


def get_db():
    return PostgreSQL(postgres_settings.POSTGRESQL_URL)
