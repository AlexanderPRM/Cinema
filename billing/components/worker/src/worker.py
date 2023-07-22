import json

import aiohttp
from core.config import config
from core.utils import generate_admin_jwt
from db.rabbit import RabbitMQBroker


class Worker:
    def __init__(self, rabbitmq_client) -> None:
        self.rabbitmq_client: RabbitMQBroker = rabbitmq_client

    async def consume_auth(self):
        await self.rabbitmq_client.connect()
        async with self.rabbitmq_client.queue.iterator() as queue_iter:
            async with aiohttp.ClientSession(
                cookies={"access_token_cookie": generate_admin_jwt()}
            ) as aio_session:
                while True:
                    async for message in queue_iter:
                        async with message.process():
                            data = json.loads(message.body.decode())
                            body = {
                                "role_name": "subscriber" if data["auto_renewal"] else "default"
                            }
                            await aio_session.put(
                                config.AUTH_SERVICE_URL
                                + "api/v1/role/change_role/{}".format(data["user_id"]),
                                data=json.dumps(body),
                                headers={"Content-Type": "application/json"},
                            )

    async def consume_emails(self):
        await self.rabbitmq_client.connect()
        async with self.rabbitmq_client.queue.iterator() as queue_iter:
            async with aiohttp.ClientSession(
                cookies={"access_token_cookie": generate_admin_jwt()}
            ) as aio_session:
                while True:
                    async for message in queue_iter:
                        async with message.process():
                            data = message.body.decode()
                            await aio_session.post(
                                config.NOTIFICATION_SERVICE_URL,
                                data=data,
                                headers={"Content-Type": "application/json"},
                            )
