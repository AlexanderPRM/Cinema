import aiohttp
import backoff
from utils.config import scheduler_settings


@backoff.on_exception(backoff.expo, Exception)
async def api_send_notification(notification):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            scheduler_settings.NOTIFICATION_SERVICE_URL, json=notification
        ) as resp:
            return await resp.text()
