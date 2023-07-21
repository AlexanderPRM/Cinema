import ipaddress
from http import HTTPStatus

from app import app
from core.config import ip_white_list, rabbit_settings
from core.jwt import JWTBearer
from db.postgres import PostgreSQL, get_db
from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse
from models.payment_models import Notification, Payment_info
from services.provider_definer import ProviderDefiner

router = APIRouter()


@router.get(
    "/get_transactions/",
    response_description="Проверить статус платежа",
    status_code=HTTPStatus.OK,
)
async def check_payment_status(
    body: Payment_info,
    psql: PostgreSQL = Depends(get_db),
    auth: dict = Depends(JWTBearer()),
):
    response = await ProviderDefiner.get_payment_info_from_provider(body.payment_id, psql)
    if not response:
        return JSONResponse({"message": "Transaction doesn't exist"}, HTTPStatus.BAD_REQUEST)
    return JSONResponse(response)


@router.post(
    "/transaction_handler/",
    response_description="Обработка вебхука от провайдера",
    status_code=HTTPStatus.OK,
)
async def webhook_processing(
    request: Request,
    psql: PostgreSQL = Depends(get_db),
):
    ip = ipaddress.ip_address(str(request.client.host))
    for provider_name, network in ip_white_list.PROVIDERS_IP_LIST.items():
        if ip in network:
            data: Notification = await ProviderDefiner.webhook_confirmation(
                request, provider_name, psql
            )
            if data is None:
                return Response(status_code=HTTPStatus.OK)

            rabbit_worker = app.state.rabbit_worker
            await rabbit_worker.send_rabbitmq(data, rabbit_settings.BILLING_QUEUE_NOTIFICATIONS)
            await rabbit_worker.send_rabbitmq(data, rabbit_settings.BILLING_QUEUE_AUTH)
            return Response(status_code=HTTPStatus.OK)
    return Response(status_code=HTTPStatus.FORBIDDEN)
