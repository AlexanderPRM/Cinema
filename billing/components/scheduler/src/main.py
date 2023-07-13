import asyncio
import logging

import asyncpg
import redis
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from core.config import postgres_settings, rabbit_settings, settings
from core.logging_setup import init_logger
from core.postgres import PostgreSQLProducer
from core.rabbit import RabbitMQBroker
from sheduler import Scheduler

init_logger()


async def taking_subscriptions_away():
    pg_connection = await asyncpg.connect(
        user=postgres_settings.POSTGRES_USER,
        password=postgres_settings.POSTGRES_PASSWORD,
        host=postgres_settings.POSTGRES_HOST,
        port=postgres_settings.POSTGRES_PORT,
        database=postgres_settings.POSTGRES_DB,
    )
    rabbitmq_client_auth = RabbitMQBroker(
        url=f"amqp://{rabbit_settings.RABBITMQ_USER}:{rabbit_settings.RABBITMQ_PASS}@{rabbit_settings.RABBITMQ_HOST}/",
        queue_name=rabbit_settings.BILLING_QUEUE_AUTH,
    )
    rabbitmq_client_notifications = RabbitMQBroker(
        url=f"amqp://{rabbit_settings.RABBITMQ_USER}:{rabbit_settings.RABBITMQ_PASS}@{rabbit_settings.RABBITMQ_HOST}/",
        queue_name=rabbit_settings.BILLING_QUEUE_NOTIFICATIONS,
    )
    r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
    await rabbitmq_client_auth.connect()
    await rabbitmq_client_notifications.connect()
    scheduler = Scheduler(
        producer=PostgreSQLProducer(pg_connection),
        auth_broker=rabbitmq_client_auth,
        notifications_broker=rabbitmq_client_notifications,
        cache=r,
    )
    logging.info("Scheduler started")
    try:
        await scheduler.taking_subs_away()
    finally:
        await pg_connection.close()
        await rabbitmq_client_auth.disconnect()
        await rabbitmq_client_notifications.disconnect()
        r.close()


if __name__ == "__main__":
    scheduler = AsyncIOScheduler()
    scheduler.add_job(taking_subscriptions_away, "interval", seconds=80)
    scheduler.start()
    asyncio.get_event_loop().run_forever()
