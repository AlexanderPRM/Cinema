import datetime
import json
from functools import lru_cache

from db.models import SubscriptionsTiers
from db.postgres import PostgreSQL, get_postgres
from db.rabbit import RabbitMQBroker, get_rabbit
from fastapi import Depends
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker


class AdminService:
    def __init__(self, pg_conn, broker):
        self.db = pg_conn
        self.asyncsession = sessionmaker(
            self.db.engine, expire_on_commit=False, class_=AsyncSession
        )
        self.broker = broker

    async def add_subscription(self, data):
        data = dict(data)
        data["created_at"] = datetime.datetime.now()
        data["updated_at"] = datetime.datetime.now()
        if data.get("discount_duration"):
            data["discount_duration"] = datetime.datetime.strptime(
                data["discount_duration"], "%Y-%m-%d %H:%M:%S"
            )
        async with self.asyncsession() as session:
            async with session.begin():
                sub = SubscriptionsTiers(**data)
                session.add(sub)
            return sub

    async def update_subscription(self, id, data):
        data = dict(data)
        data["id"] = id
        data["updated_at"] = datetime.datetime.now()
        if data.get("discount_duration"):
            data["discount_duration"] = datetime.datetime.strptime(
                data["discount_duration"], "%Y-%m-%d %H:%M:%S"
            )
        async with self.asyncsession() as session:
            async with session.begin():
                stmt = update(SubscriptionsTiers).where(SubscriptionsTiers.id == id).values(data)
                await session.execute(stmt)
        users = await self.db.get_all_users_with_sub(subscribe_id=id)
        await self.db.disable_auto_renewal(subscribe_id=id)
        users_list = []
        for user in users:
            body = json.dumps(
                {
                    "user_id": str(user.user_id),
                    "subscribe_id": str(id),
                    "operation": "disable auto-renewal + update sub",
                }
            )
            # notification
            await self.broker.send_data(body)
            users_list.append(str(user.user_id))
        return users_list

    async def get_transactions(self, page_size, page_number):
        data = await self.db.get_transactions_list(page_size, page_number)
        return data

    async def get_user_transactions(self, page_size, page_number, user_id):
        data = await self.db.get_user_transactions_list(page_size, page_number, user_id)
        return data


@lru_cache()
def get_service(
    postgres: PostgreSQL = Depends(get_postgres), broker: RabbitMQBroker = Depends(get_rabbit)
) -> AdminService:
    return AdminService(postgres, broker)
