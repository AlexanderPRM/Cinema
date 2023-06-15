from core.config import rabbit_settings
from db.rabbitmq import RabbitWorker
from fastapi import APIRouter
from models.notification import Notification

router = APIRouter()


@router.post(
    "/send/",
    summary="Уведомления",
    description="Отправить уведомление в очередь RabbitMQ",
)
async def add_to_rabbit(
    notification: Notification,
):
    await RabbitWorker().send_rabbitmq(notification.dict(), rabbit_settings.EMAIL_QUEUE)
    return {"message": "OK"}
