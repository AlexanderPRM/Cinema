from uuid import UUID

from core.config import config
from core.jwt import JWTBearer
from db.postgres import PostgreSQL, get_db
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from models.billing import Confirmation, Message, Pay, PayResponse, UnsubscribeResponse
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
            content={"message": "Subscription Tier not Found."},
        )
    payment_data = {
        "amount": {"value": subscribe_tier.cost, "currency": body.currency},
        "confirmation": {"type": "redirect", "return_url": config.PAYMENT_REDIRECT_URL},
        "capture": True,
        "description": "Заказ на оплату подписки под номером %s пользователя %s"
        % (subscribe_tier.id, auth["user_id"]),
        "save_payment_method": body.auto_renewal,
    }
    pay_response = provider.pay(payment_data, body.idempotence_key)
    if not pay_response:
        raise JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"message": "This Idempotency Key has expired for Today"},
        )
    transaction = {
        "user_id": auth["user_id"],
        "transaction_id": pay_response.id,
        "value": pay_response.amount.value,
        "currency": pay_response.amount.currency,
        "provider": "yookassa",
        "idempotency_key": body.idempotence_key,
        "operate_status": "waiting",
    }
    await postgres.insert_transaction(transaction)
    return PayResponse(
        confirmation=Confirmation(
            confirmation_url=pay_response.confirmation.confirmation_url,
            type=pay_response.confirmation.type,
        ),
        created_at=pay_response.created_at,
    )


@router.post(
    "/unsubscribe/",
    response_model=UnsubscribeResponse,
    status_code=status.HTTP_200_OK,
    responses={403: {"model": Message}},
    summary="Отписка от автопродления.",
    description="Отписка от автопродления для пользователя.",
)
async def unsubscribe(
    auth: dict = Depends(JWTBearer()),
    postgres: PostgreSQL = Depends(get_db),
):
    subscription = await postgres.get_subscibe_by_user(auth["user_id"])
    if not subscription:
        raise JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"message": "User doesn't have a subscription"},
        )
    idx = await postgres.update_auto_renewal_subscribe_by_user(auth["user_id"])
    return {"message": "OK", "subscribe_id": idx}
