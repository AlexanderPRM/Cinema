import aio_pika
import backoff
from aio_pika import exceptions
from core.config import rabbit_settings


class RabbitConsumer:
    def __init__(self):
        self.connection = None
        self.channel = None

    @backoff.on_exception(backoff.expo, exceptions.CONNECTION_EXCEPTIONS, max_tries=5, max_time=15)
    async def get_connection(self):
        if self.connection is None:
            self.connection = await aio_pika.connect_robust(
                f"amqp://{rabbit_settings.NOTF_RABBITMQ_USER}:{rabbit_settings.NOTF_RABBITMQ_PASS}"
                f"@{rabbit_settings.NOTF_RABBITMQ_HOST}:{rabbit_settings.NOTF_RABBITMQ_PORT}/",
                timeout=10.0,
            )
        return self.connection

    @backoff.on_exception(backoff.expo, exceptions.CONNECTION_EXCEPTIONS, max_tries=5, max_time=15)
    async def get_channel(self):
        if self.connection is None:
            self.get_connection()
        if self.channel is None:
            self.channel = await self.connection.channel()
        return self.channel
