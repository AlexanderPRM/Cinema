import asyncio

from core.config import rabbit_settings
from db.rabbit import RabbitMQBroker
from worker import Worker


async def main():
    client = Worker(
        rabbitmq_client=RabbitMQBroker(
            url=f"amqp://{rabbit_settings.RABBITMQ_USER}:{rabbit_settings.RABBITMQ_PASS}@"
            f"{rabbit_settings.RABBITMQ_HOST}/",
            queue_name=rabbit_settings.BILLING_QUEUE_AUTH,
        )
    )
    await client.consume_auth()


if __name__ == "__main__":
    asyncio.run(main())
