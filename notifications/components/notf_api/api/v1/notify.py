from http import HTTPStatus

from app import app
from core.config import rabbit_settings
from core.jwt import JWTBearer
from db.postgres import PostgreSQL, get_db
from fastapi import APIRouter, Depends
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


@router.post("/mailing_subscription/")
async def mailing_subscription(
    auth: dict = Depends(JWTBearer()), postgres: PostgreSQL = Depends(get_db)
):
    find_user = await postgres.get_user(auth["user_id"])
    if find_user:
        await postgres.return_subscribe_for_user(auth["user_id"])
        return {"message": "Subscribe ON"}, HTTPStatus.OK
    else:
        await postgres.unsubscribe_user(auth["user_id"])
        return {"message": "Subscribe OFF"}, HTTPStatus.OK
