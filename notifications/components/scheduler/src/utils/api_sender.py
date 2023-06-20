import aiohttp
import backoff
from utils.logger import logger


@backoff.on_exception(backoff.expo, Exception)
async def api_send_notification(notification):

    url = "http://notifications-notification_api-1:8001/api/v1/notify/send/"
    async with aiohttp.ClientSession() as session:
        logger.info("Sent http request")
        async with session.post(url, json=notification) as resp:
            return await resp.text()
