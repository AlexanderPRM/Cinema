import asyncio
import logging

import asyncpg
from apscheduler.schedulers.asyncio import AsyncIOScheduler
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


if __name__ == "__main__":
    scheduler = AsyncIOScheduler()
    scheduler.add_job(collect_likes, 'interval', seconds=60)
    scheduler.start()
    asyncio.get_event_loop().run_forever()
