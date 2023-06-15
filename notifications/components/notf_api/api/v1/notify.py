from app import app
from core.config import rabbit_settings
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
    rabbit_worker = app.state.rabbit_worker
    await rabbit_worker.send_rabbitmq(notification.dict(), rabbit_settings.EMAIL_QUEUE)
    return {"message": "OK"}
