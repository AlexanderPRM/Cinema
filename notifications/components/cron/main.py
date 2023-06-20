# import asyncpg
# from core.config import postgres_settings, rabbit_settings, worker_setting
# from db.postgres import PostgreSQLConsumer
# from db.rabbitmq import RabbitConsumer

import asyncio
import logging

import asyncpg
import schedule
from core.config import postgres_settings
from core.logging_setup import init_logger
from cron import Cron
from db.postgres import PostgreSQLConsumer

init_logger()


async def collect_likes():
    client = Cron(
        postgres_client=PostgreSQLConsumer(
            await asyncpg.connect(
                user=postgres_settings.NOTF_POSTGRES_USER,
                password=postgres_settings.NOTF_POSTGRES_PASSWORD,
                host=postgres_settings.NOTF_POSTGRES_HOST,
                port=postgres_settings.NOTF_POSTGRES_PORT,
                database=postgres_settings.NOTF_POSTGRES_DB,
            )
        ),
    )
    logging.info("--CRON RUNNING-- Collecting likes")
    await client.collect()


def wrapper(coro):
    asyncio.create_task(coro())


schedule.every(60).seconds.do(wrapper, collect_likes)


async def main():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
