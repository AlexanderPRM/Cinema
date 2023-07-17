from uuid import UUID

from core.config import config
from core.jwt import JWTBearer
from db.postgres import PostgreSQL, get_db
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from models.billing import Confirmation, Message, Pay, PayResponse
from providers.base import Provider
from providers.yookassa_provider import get_yookassa

router = APIRouter()


@router.post(
    "/pay/{subscribe_plan_id}/",
    response_model=PayResponse,
    status_code=status.HTTP_201_CREATED,
    responses={404: {"model": Message}},
    response_description="Пример информации о платежа с ссылкой для оплаты.",
    summary="Оплата подписки.",
    description="Оплата подписки по какому-то выбранному плану.",
)
async def pay(
    subscribe_plan_id: UUID,
    body: Pay,
    auth: dict = Depends(JWTBearer()),
    postgres: PostgreSQL = Depends(get_db),
    provider: Provider = Depends(get_yookassa),
):
    subscribe_tier = await postgres.get_subscribe_tier(subscribe_plan_id)
    if not subscribe_tier:
        raise JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Subscription Tier not Found."},
        )
    payment_data = {
        "amount": {"value": subscribe_tier.cost, "currency": body.currency},
        "confirmation": {"type": "redirect", "return_url": config.PAYMENT_REDIRECT_URL},
        "capture": True,
        "description": "Заказ на оплату подписки под номером %s пользователя %s"
        % (subscribe_tier.id, auth["user_id"]),
        "save_payment_method": body.auto_renewal,
    }
    ans = provider.pay(payment_data, body.idempotence_key)
    transaction = {
        "user_id": auth["user_id"],
        "transaction_id": ans.id,
        "value": ans.amount.value,
        "currency": ans.amount.currency,
        "provider": "yookassa",
        "idempotency_key": body.idempotence_key,
        "operate_status": "waiting",
    }
    await postgres.insert_transaction(transaction)
    return PayResponse(
        confirmation=Confirmation(
            confirmation_url=ans.confirmation.confirmation_url, type=ans.confirmation.type
        ),
        created_at=ans.created_at,
    )
