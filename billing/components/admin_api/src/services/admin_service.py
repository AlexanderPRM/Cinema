import datetime
import logging
import uuid
from functools import lru_cache

from core.models import Subscriptions, TransactionsLog
from core.postgres import PostgreSQL, get_postgres
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class AdminService:
    def __init__(self, pg_conn):
        self.db = pg_conn

    async def add_subscription(self, data):
        data = dict(data)
        data["subscribe_id"] = uuid.uuid4()
        data["created_at"] = datetime.datetime.now()
        data["updated_at"] = datetime.datetime.now()
        data["duratation"] = datetime.datetime.strptime(
            data["duratation"], "%Y, %m, %d, %H, %M, %S, %f"
        )
        if data["discount_duratation"]:
            data["discount_duratation"] = datetime.datetime.strptime(
                data["discount_duratation"], "%Y, %m, %d, %H, %M, %S, %f"
            )
        sub = Subscriptions(**data)
        async with AsyncSession(self.db.engine) as session:
            session.add(sub)
            await session.commit()
        return sub

    async def get_transactions(self, page_size, page_number):
        data = await self.db.get_transactions_list(page_size, page_number)
        return data


@lru_cache()
def get_service(
    postgres: PostgreSQL = Depends(get_postgres),
) -> AdminService:
    return AdminService(postgres)
