import asyncio
import os

import asyncpg
from core.config import postgres_settings
from db.postgres import PostgreSQLConsumer
from db.rabbitmq import RabbitConsumer
from worker import Worker


async def main():
    client = Worker(
        os.getenv("NOTF_ELASTICEMAIL_API_KEY"),
        os.getenv("NOTF_ELASTICEMAIL_FROM_EMAIL"),
        RabbitConsumer(),
        PostgreSQLConsumer(
            await asyncpg.connect(
                user=postgres_settings.NOTF_POSTGRES_USER,
                password=postgres_settings.NOTF_POSTGRES_PASSWORD,
                host=postgres_settings.NOTF_POSTGRES_HOST,
                port=postgres_settings.NOTF_POSTGRES_PORT,
                database=postgres_settings.NOTF_POSTGRES_DB,
            )
        ),
    )
    await client.consume()


if __name__ == "__main__":
    asyncio.run(main())
