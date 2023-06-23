import logging

import aiohttp
import backoff
from core.config import cron_setting
from core.utils import generate_admin_jwt
from db.postgres import PostgreSQLConsumer


class Cron:
    def __init__(self, postgres_client) -> None:
        self.postgres_client: PostgreSQLConsumer = postgres_client

    @backoff.on_exception(backoff.expo, aiohttp.ClientError, max_tries=5)
    async def get_likes_notification(self, aio_session):
        async with aio_session.get(cron_setting.UGC_URL + "review/") as resp:
            return await resp.json()

    @backoff.on_exception(backoff.expo, aiohttp.ClientError, max_tries=5)
    async def get_author_review(self, aio_session, review_id):
        async with aio_session.get(cron_setting.UGC_URL + f"review/author/{review_id}") as resp:
            return await resp.json()

    @backoff.on_exception(backoff.expo, aiohttp.ClientError, max_tries=5)
    async def get_last_liked_user(self, aio_session, review_id):
        async with aio_session.get(cron_setting.UGC_URL + f"review/last_liked/{review_id}") as resp:
            return await resp.json()

    async def collect(self):
        async with aiohttp.ClientSession(
            cookies={"access_token_cookie": generate_admin_jwt()}
        ) as aio_session:
            likes = await self.get_likes_notification(aio_session)
            if likes is None:
                return
            logging.info(likes)
            for like in likes.get("data"):
                data = {
                    "context": {
                        "users_id": [],
                        "payload": {"last_liked_user": {}},
                        "link": cron_setting.SITE_LINK,
                    }
                }
                review_id = like.get("review_id")
                author_id = await self.get_author_review(aio_session, review_id)
                logging.info(author_id)
                data["context"]["users_id"].append(author_id.get("author"))
                last_liked_user = await self.get_last_liked_user(aio_session, review_id)
                data["context"]["payload"]["last_liked_user"]["id"] = last_liked_user.get(
                    "Last liked by user"
                )
                data["context"]["payload"]["likes"] = like.get("likes")
                logging.info(data)
                await self.postgres_client.insert_task(data)
