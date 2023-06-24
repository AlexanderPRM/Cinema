import json
import logging
from http import HTTPStatus

import aiohttp
import ElasticEmail
from core.config import rabbit_settings, worker_setting
from core.utils import generate_admin_jwt
from db.postgres import PostgreSQLConsumer
from db.rabbitmq import RabbitConsumer
from ElasticEmail.api import emails_api
from ElasticEmail.models import (
    BodyContentType,
    BodyPart,
    EmailContent,
    EmailMessageData,
    EmailRecipient,
)


class Worker:
    def __init__(self, api_key, from_email, rabbitmq_client, postgres_client) -> None:
        self.configuration = ElasticEmail.Configuration()
        self.configuration.api_key["apikey"] = api_key
        self.sender = from_email
        self.rabbitmq_client: RabbitConsumer = rabbitmq_client
        self.postgres_client: PostgreSQLConsumer = postgres_client

    async def build_confirm_email_recipients(self, user_info, message):
        return [
            EmailRecipient(
                email=user_info["email"],
                fields={
                    "name": user_info["name"] if user_info["name"] else "Guest",
                    "confirmation_link": message["context"]["link"],
                },
            )
        ]

    async def build_film_distribution_recipients(self, user_info, message, recipients):
        fields = {
            "name": user_info["name"] if user_info["name"] else "Guest",
            "url": message["context"]["link"],
        }
        counter = 1
        for film in message["context"]["payload"]["film_list"]:
            fields.update({f"film_name_{counter}": film["name"]})
            counter += 1
        recipients.append(EmailRecipient(email=user_info["email"], fields=fields))

    async def build_review_like(self, user_info, last_liked_name, message):
        fields = {
            "author": user_info["name"] if user_info["name"] else "Guest",
            "user": last_liked_name if last_liked_name else "Anonim",
            "likes": message["context"]["payload"]["likes"],
            "url": message["context"]["link"],
        }
        return [EmailRecipient(email=user_info["email"], fields=fields)]

    async def build_mail(self, recipients, subject, content):
        email_message_data = EmailMessageData(
            recipients=recipients,
            content=EmailContent(
                body=[
                    BodyPart(
                        content_type=BodyContentType("HTML"), content=content, charset="utf-8"
                    ),
                    BodyPart(
                        content_type=BodyContentType("PlainText"), content=content, charset="utf-8"
                    ),
                ],
                _from=self.sender,
                subject=subject,
            ),
        )
        return email_message_data

    async def send_mail(self, elasticemail_api, mail):
        email_instance = emails_api.EmailsApi(elasticemail_api)
        return email_instance.emails_post(mail)

    async def consume(self):
        with ElasticEmail.ApiClient(self.configuration) as elasticemail_api:
            async with await self.rabbitmq_client.get_connection():
                channel = await self.rabbitmq_client.get_channel()
                async with aiohttp.ClientSession(
                    cookies={"access_token_cookie": generate_admin_jwt()}
                ) as aio_session:
                    async for message in await channel.declare_queue(
                        rabbit_settings.EMAIL_QUEUE, durable=True
                    ):
                        message = json.loads(message.body.decode())
                        db_template = await self.postgres_client.get_template(
                            message["template_id"]
                        )
                        recipients = []
                        for user_id in message["context"]["users_id"]:
                            aio_response = await aio_session.get(
                                worker_setting.AUTH_URL + f"get_user_info/{user_id}/"
                            )
                            user_info = await aio_response.json()
                            print(user_info)
                            if aio_response.status != HTTPStatus.FORBIDDEN:
                                if message["type_send"] == "email_confirm":
                                    recipients = await self.build_confirm_email_recipients(
                                        user_info, message
                                    )
                                elif message["type_send"] in ("new_episodes", "recommendations"):
                                    if not self.postgres_client.get_subscribe_user(user_id):
                                        await self.build_film_distribution_recipients(
                                            user_info, message, recipients
                                        )
                                elif message["type_send"] == "person_likes":
                                    last_liked_info = await aio_session.get(
                                        worker_setting.AUTH_URL
                                        + f"get_user_info/ \
                                        {message['context']['payload']['last_liked_user']['id']}/"
                                    )
                                    last_liked_info = await last_liked_info.json()
                                    last_liked_name = last_liked_info.get("name")
                                    recipients = await self.build_review_like(
                                        user_info, last_liked_name, message
                                    )
                        if recipients:
                            mail = await self.build_mail(
                                recipients,
                                db_template[0]["title"],
                                db_template[0]["template_text"],
                            )
                            response = await self.send_mail(elasticemail_api, mail)
                            logging.info(response)
