from typing import Dict, List, Optional
from uuid import UUID

from core.jwt import JWTBearer
from core.logger import logger
from core.utils import CommonQueryParams
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from models.responses import AddSubscribtion, UpdateSub
from models.subscribtion import Subscribtion
from models.transaction import Transaction
from services.admin_service import AdminService, get_service

router = APIRouter()


@router.post(
    "/add/",
    response_model=AddSubscribtion,
    response_description="Пример создания нового тарифного плана.",
    summary="Создать тарифный план.",
    description="Создание тарифного плана.",
)
async def add_subscribtion(
    body: Subscribtion,
    auth: dict = Depends(JWTBearer()),
    service: AdminService = Depends(get_service),
):
    if auth["role"] != "superuser":
        return JSONResponse({"message": "Superuser only"}, status.HTTP_403_FORBIDDEN)
    entry_id = await service.add_subscription(body)
    response = {
        "message": f"{body.title} subscription created.",
        "subscribe_id": str(entry_id.id),
    }
    return AddSubscribtion(**response)


@router.get(
    "/transactions/",
    response_model=List[Transaction],
    response_description="Пример получения списка транзакций.",
    summary="Получить список транзакций.",
    description="Получение списка транзакций с пагинацией.",
)
async def get_list_transactions(
    commons: CommonQueryParams = Depends(CommonQueryParams),
    auth: dict = Depends(JWTBearer()),
    service: AdminService = Depends(get_service),
) -> Optional[List[Dict[str, Transaction]]]:
    if auth["role"] != "superuser":
        return JSONResponse({"message": "Superuser only"}, status.HTTP_403_FORBIDDEN)
    transactions = await service.get_transactions(
        page_size=commons.page_size, page_number=commons.page_number
    )
    if not transactions:
        return JSONResponse("No transactions")
    logger.info(transactions)
    transaction_objs = [
        Transaction(
            user_id=transaction.user_id,
            transaction_id=transaction.transaction_id,
            value=transaction.value,
            provider=transaction.provider,
            currency=transaction.currency,
            idempotency_key=transaction.idempotency_key,
            operate_status=transaction.operate_status,
            payment_details=transaction.payment_details,
            created_at=transaction.created_at,
            updated_at=transaction.updated_at,
        )
        for transaction in transactions
    ]
    return transaction_objs


@router.get(
    "/transactions/{user_id}/",
    response_model=List[Transaction],
    response_description="Пример получения списка транзакций пользователя.",
    summary="Получить список транзакций пользователя.",
    description="Получение списка транзакций пользователя с пагинацией.",
)
async def get_user_list_transactions(
    user_id: UUID,
    commons: CommonQueryParams = Depends(CommonQueryParams),
    auth: dict = Depends(JWTBearer()),
    service: AdminService = Depends(get_service),
) -> Optional[List[Dict[str, Transaction]]]:
    if auth["role"] != "superuser":
        return JSONResponse({"message": "Superuser only"}, status.HTTP_403_FORBIDDEN)
    transactions = await service.get_user_transactions(
        page_size=commons.page_size, page_number=commons.page_number, user_id=user_id
    )
    if not transactions:
        return JSONResponse("No transactions")
    transaction_objs = [
        Transaction(
            user_id=transaction.user_id,
            transaction_id=transaction.transaction_id,
            value=transaction.value,
            provider=transaction.provider,
            currency=transaction.currency,
            idempotency_key=transaction.idempotency_key,
            operate_status=transaction.operate_status,
            payment_details=transaction.payment_details,
            created_at=transaction.created_at,
            updated_at=transaction.updated_at,
        )
        for transaction in transactions
    ]
    return transaction_objs


@router.put(
    "/update/{sub_id}/",
    response_model=UpdateSub,
    response_description="Изменение плана подписки.",
    summary="Изменение тарифного плана подписки.",
    description="Изменение тарифного плана подписки.",
)
async def update_sub(
    body: Subscribtion,
    sub_id: UUID,
    auth: dict = Depends(JWTBearer()),
    service: AdminService = Depends(get_service),
):
    if auth["role"] != "superuser":
        return JSONResponse({"message": "Superuser only"}, status.HTTP_403_FORBIDDEN)
    result = await service.update_subscription(id=sub_id, data=body)
    response = {
        "message": "Succesfully update subscription",
        "users_autorenewal_disabled": [user for user in result],
    }
    return UpdateSub(**response)
