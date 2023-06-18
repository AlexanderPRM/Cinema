import json
import logging

import aiohttp
import ElasticEmail
import jinja2
from core.config import rabbit_settings, worker_setting
from core.utils import generate_admin_jwt
from db.postgres import PostgreSQLConsumer
from db.rabbitmq import RabbitConsumer
from ElasticEmail.api import emails_api
from ElasticEmail.models import EmailMessageData, EmailRecipient


class Worker:
    def __init__(self, api_key, from_email, rabbitmq_client, postgres_client) -> None:
        configuration = ElasticEmail.Configuration()
        configuration.api_key["apikey"] = api_key
        self.elasticmail_api = ElasticEmail.ApiClient(configuration)
        self.email_api = emails_api.EmailsApi(self.elasticmail_api)
        self.sender = from_email
        self.rabbitmq_client: RabbitConsumer = rabbitmq_client
        self.postgres_client: PostgreSQLConsumer = postgres_client

    async def template_processing(self, template, body):
        jinja_template = jinja2.Template(template["template_text"])
        output_template = jinja_template.render(**body)
        return output_template

    async def build_mail(self, email, subject, content):
        email_message_data = EmailMessageData(
            recipients=[EmailRecipient(email=email)],
            content={
                "Body": [{"ContentType": "HTML", "Content": content}],
                "Subject": subject,
                "From": self.sender,
            },
        )
        return email_message_data

    async def send_mail(self, mail):
        return self.email_api.emails_post(mail)

    async def consume(self):
        async with await self.rabbitmq_client.get_connection():
            channel = await self.rabbitmq_client.get_channel()
            async with aiohttp.ClientSession(
                cookies={"access_token_cookie": generate_admin_jwt()}
            ) as aio_session:
                async for message in await channel.declare_queue(
                    rabbit_settings.EMAIL_QUEUE, durable=True
                ):
                    message = json.loads(message.body.decode())
                    db_template = await self.postgres_client.get_template(message["template_id"])
                    users_info = []
                    for user_id in message["context"]["users_id"]:
                        user_info = await aio_session.get(
                            worker_setting.AUTH_URL + f"get_user_info/{user_id}/"
                        )
                        users_info.append(await user_info.json())
                    if message["type_send"] == "email_confirm":
                        user = users_info[0]
                        body = {
                            "name": user["name"] if user["name"] else "Guest",
                            "confirmation_link": message["context"]["link"],
                        }
                        output_template = await self.template_processing(db_template[0], body)
                        mail = await self.build_mail(
                            user["email"], db_template[0]["title"], output_template
                        )
                        response = await self.send_mail(mail)
                        logging.info(response)
