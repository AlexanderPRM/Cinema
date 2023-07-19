import aio_pika


class RabbitMQBroker:
    def __init__(self, url, queue_name):
        self.url = url
        self.queue_name = queue_name

    async def connect(self):
        # Establishing a connection to the RabbitMQ server
        self.connection = await aio_pika.connect_robust(self.url)
        self.channel = await self.connection.channel()
        self.queue = await self.channel.declare_queue(self.queue_name, durable=True)

    async def disconnect(self):
        # Closing the connection to the RabbitMQ server
        await self.connection.close()

    async def send_data(self, data):
        await self.channel.default_exchange.publish(
            aio_pika.Message(data.encode(), delivery_mode=aio_pika.DeliveryMode.PERSISTENT),
            routing_key=self.queue.name,
        )

    async def receive_data(self):
        async with self.queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    data = message.body.decode()
                    return data
