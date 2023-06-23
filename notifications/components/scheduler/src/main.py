import asyncio
import json

from db.pg_notifier import PostgresNotifier
from utils.api_sender import api_send_notification
from utils.config import scheduler_settings
from utils.logger import logger
from utils.models import FilmContext, FilmsNotification, LikeContext, LikesNotification


class Scheduler:
    def __init__(self):
        self.pg_nf = None

    async def start(self):
        self.pg_nf = PostgresNotifier()
        await self.pg_nf.create_connection()

        await asyncio.gather(
            self.new_episodes_control(scheduler_settings.NEW_EPISODES),
            self.weekly_recommendations_control(scheduler_settings.RECOMMENDATIONS),
            self.person_likes_control(scheduler_settings.PERSON_LIKES),
            return_exceptions=True,
        )

    async def new_episodes_control(self, task_type: str):
        while True:
            try:
                result = await self.pg_nf.get_notification(task_type)
                if result:
                    data = [{key: value for key, value in item.items()} for item in result]
                    logger.info(data)
                    for item in data:
                        params = json.loads(item.get("task_data"))
                        context = FilmContext(
                            users_id=params.get("context").get("users_id"),
                            payload=params.get("context").get("payload"),
                            link=params.get("context").get("link"),
                        )
                        notification = FilmsNotification(
                            type_send=item.get("task_type"),
                            context=context,
                            template_id=str(item.get("template_id")),
                            notification_id=str(item.get("task_id")),
                        )
                        resp = await api_send_notification(notification.dict())
                        status = json.loads(resp).get("message")
                        if status == "OK":
                            await self.pg_nf.set_status(item.get("task_id"))

                await asyncio.sleep(scheduler_settings.RECOMMENDATIONS_TIMEOUT)

            except Exception as error:
                logger.error(error)
                raise error

    async def weekly_recommendations_control(self, task_type: str):
        while True:
            try:
                result = await self.pg_nf.get_notification(task_type)
                if result:
                    data = [{key: value for key, value in item.items()} for item in result]
                    logger.info(data)
                    for item in data:
                        params = json.loads(item.get("task_data"))

                        context = FilmContext(
                            users_id=params.get("context").get("users_id"),
                            payload=params.get("context").get("payload"),
                            link=params.get("context").get("link"),
                        )
                        notification = FilmsNotification(
                            type_send=item.get("task_type"),
                            context=context,
                            template_id=str(item.get("template_id")),
                            notification_id=str(item.get("task_id")),
                            category_name=item.get("category_name"),
                        )
                        resp = await api_send_notification(notification.dict())
                        status = json.loads(resp).get("message")
                        if status == "OK":
                            await self.pg_nf.set_status(item.get("task_id"))

                await asyncio.sleep(scheduler_settings.RECOMMENDATIONS_TIMEOUT)

            except Exception as error:
                logger.error(error)
                raise error

    async def person_likes_control(self, task_type: str):
        while True:
            try:
                result = await self.pg_nf.get_notification(task_type)
                if result:
                    data = [{key: value for key, value in item.items()} for item in result]
                    logger.info(data)
                    for item in data:
                        params = json.loads(item.get("task_data"))

                        context = LikeContext(
                            users_id=params.get("context").get("users_id"),
                            payload=params.get("context").get("payload"),
                            link=params.get("context").get("link"),
                        )
                        notification = LikesNotification(
                            type_send=item.get("task_type"),
                            context=context,
                            template_id=str(item.get("template_id")),
                            notification_id=str(item.get("task_id")),
                            category_name=item.get("category_name"),
                        )
                        resp = await api_send_notification(notification.dict())
                        status = json.loads(resp).get("message")
                        if status == "OK":
                            await self.pg_nf.set_status(item.get("task_id"))

                await asyncio.sleep(scheduler_settings.RECOMMENDATIONS_TIMEOUT)

            except Exception as error:
                logger.error(error)
                raise error


if __name__ == "__main__":
    asyncio.run(Scheduler().start())
