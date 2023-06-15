import json

import aio_pika
from aio_pika import ExchangeType, Message
from core.config import rabbit_settings


class RabbitWorker:
    def __init__(self):
        self.connection = None

    async def get_connection(self):
        if self.connection is None:
            self.connection = await aio_pika.connect_robust(
                f"amqp://{rabbit_settings.RABBITMQ_USER}:{rabbit_settings.RABBITMQ_PASS}"
                f"@{rabbit_settings.RABBITMQ_HOST}:{rabbit_settings.RABBITMQ_PORT}/",
                timeout=10.0,
            )
        return self.connection

    async def send_rabbitmq(self, msg=dict, queue=str):
        connection = await self.get_connection()
        channel = await connection.channel()
        await channel.default_exchange.publish(
            Message(json.dumps(msg).encode("utf-8")), routing_key=queue
        )

    async def make_queues(self):
        connection = await self.get_connection()
        channel = await connection.channel()
        email_exchange = await channel.declare_exchange(
            rabbit_settings.EMAIL_EXCHANGE, ExchangeType.DIRECT, durable=True
        )
        send_email_queue = await channel.declare_queue(rabbit_settings.EMAIL_QUEUE, durable=True)
        await send_email_queue.bind(email_exchange)

    async def close_connection(self):
        if self.connection is not None:
            await self.connection.close()
