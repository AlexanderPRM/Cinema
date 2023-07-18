import time
from uuid import UUID

from core.config import config
from core.jwt import JWTBearer
from db.postgres import PostgreSQL, get_db
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from models.billing import (
    Amount,
    Confirmation,
    Message,
    Pay,
    PayResponse,
    Refund,
    RefundResponse,
    UnsubscribeResponse,
)
from providers.base import Provider
from providers.yookassa_provider import get_yookassa

router = APIRouter()


@router.post(
    "/pay/{subscribe_plan_id}/",
    response_model=PayResponse,
    status_code=status.HTTP_201_CREATED,
    responses={404: {"model": Message}, 400: {"model": Message}},
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
        return JSONResponse(
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
    if pay_response is None or pay_response.status != "pending":
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": "This Idempotency Key has expired for today OR Payment already happen"
            },
        )
    transaction = {
        "user_id": auth["user_id"],
        "transaction_id": pay_response.id,
        "value": pay_response.amount.value,
        "currency": pay_response.amount.currency,
        "payment_details": {
            "subscribe_tier_id": str(subscribe_tier.id),
            "auto_renewal": body.auto_renewal,
        },
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
    "/refund/",
    response_model=RefundResponse,
    status_code=status.HTTP_200_OK,
    response_description="Пример информации о совершённом возврате.",
    summary="Возврат оставших средств от использования подписки.",
    description="Возврат средств.",
)
async def refund(
    body: Refund,
    auth: dict = Depends(JWTBearer()),
    postgres: PostgreSQL = Depends(get_db),
    provider: Provider = Depends(get_yookassa),
):
    subscribe = await postgres.get_subscibe_by_user(auth["user_id"])
    now_time = time.time()
    if not subscribe and subscribe.ttl <= now_time:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"message": "User does not have a subscription OR it has expired."},
        )
    transaction = await postgres.get_transaction_by_id(subscribe.transaction_id)
    subscribe_tier = await postgres.get_subscribe_tier(subscribe.subscription_tier_id)
    used_seconds = subscribe.ttl - now_time
    cost_per_second = subscribe_tier.cost / subscribe_tier.duration
    refund_details = {
        "amount": {"value": cost_per_second * used_seconds, "currency": transaction.currency},
        "payment_id": transaction.id,
    }
    refund = provider.refund(refund_details, body.idempotence_key)
    return RefundResponse(
        refund.status,
        amount=Amount(value=refund.amount.value, currency=refund.amount.currency),
        payment_id=refund.payment_id,
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
