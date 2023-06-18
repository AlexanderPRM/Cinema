import asyncio

import asyncpg
from core.config import postgres_settings, worker_setting
from db.postgres import PostgreSQLConsumer
from db.rabbitmq import RabbitConsumer
from worker import Worker


async def main():
    client = Worker(
        api_key=worker_setting.NOTF_ELASTICEMAIL_API_KEY,
        from_email=worker_setting.NOTF_ELASTICEMAIL_FROM_EMAIL,
        rabbitmq_client=RabbitConsumer(),
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
    await client.consume()


if __name__ == "__main__":
    asyncio.run(main())
