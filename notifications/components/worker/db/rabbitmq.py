import aio_pika
import backoff
from aio_pika import exceptions


class RabbitConsumer:
    def __init__(self, dsn):
        self.dsn = dsn
        self.connection = None
        self.channel = None

    @backoff.on_exception(backoff.expo, exceptions.CONNECTION_EXCEPTIONS, max_tries=5, max_time=15)
    async def get_connection(self):
        if self.connection is None:
            self.connection = await aio_pika.connect_robust(
                self.dsn,
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
