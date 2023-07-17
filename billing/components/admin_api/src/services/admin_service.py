import datetime
from functools import lru_cache

from db.models import Subscriptions
from db.postgres import PostgreSQL, get_postgres
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker


class AdminService:
    def __init__(self, pg_conn):
        self.db = pg_conn
        self.asyncsession = sessionmaker(
            self.db.engine, expire_on_commit=False, class_=AsyncSession
        )

    async def add_subscription(self, data):
        data = dict(data)
        data["created_at"] = datetime.datetime.now()
        data["updated_at"] = datetime.datetime.now()
        if data.get("discount_duration"):
            data["discount_duration"] = datetime.datetime.strptime(
                data["discount_duration"], "%Y, %m, %d, %H, %M, %S, %f"
            )
        async with self.asyncsession() as session:
            async with session.begin():
                sub = Subscriptions(**data)
                session.add(sub)
            return sub

    async def get_transactions(self, page_size, page_number):
        data = await self.db.get_transactions_list(page_size, page_number)
        return data


@lru_cache()
def get_service(
    postgres: PostgreSQL = Depends(get_postgres),
) -> AdminService:
    return AdminService(postgres)
