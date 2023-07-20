import ipaddress
from http import HTTPStatus

from core.config import ip_white_list, rabbit_settings
from core.jwt import JWTBearer
from db.postgres import get_db
from main import app
from models.payment_models import Notification
from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse
from models.payment_models import Payment_info
from services.provider_definer import ProviderDefiner

router = APIRouter()


@router.get(
    "/get_transactions/",
    response_description="Проверить статус платежа",
    status_code=HTTPStatus.OK,
)
async def check_payment_status(
    body: Payment_info,
    psql = Depends(get_db),
    auth: dict = Depends(JWTBearer()),
):
    response = ProviderDefiner.get_payment_info_from_provider(body.payment_id, psql)
    return JSONResponse(response)


@router.post(
    "/transaction_handler/",
    response_description="Обработка вебхука от провайдера",
    status_code=HTTPStatus.OK,
)
async def webhook_processing(
    request: Request,
    psql = Depends(get_db),
):
    ip = ipaddress.ip_address(str(request.client.host))
    for provider_name, network in ip_white_list.PROVIDERS_IP_LIST.items():
        if any(ip in network):
            data = ProviderDefiner.webhook_confirmation(request, provider_name, psql)
            if data is None:
                return

            rabbit_worker = app.state.rabbit_worker
            await rabbit_worker.send_rabbitmq(data, rabbit_settings.BILLING_QUEUE_NOTIFICATIONS)
            await rabbit_worker.send_rabbitmq(data, rabbit_settings.BILLING_QUEUE_AUTH)
            return
    return Response(status_code=HTTPStatus.FORBIDDEN)
