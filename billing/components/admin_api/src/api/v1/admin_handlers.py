import json
from typing import Dict, List, Optional
from uuid import UUID

from core.jwt import JWTBearer
from core.utils import CommonQueryParams
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from models.subscribtion import Subscribtion
from models.transaction import Transaction
from services.admin_service import AdminService, get_service

router = APIRouter()


@router.post(
    "/add",
    response_model=None,
    response_description="Пример создания нового тарифного плана.",
    summary="Создать тарифный план.",
    description="Создание тарифного плана.",
)
async def add_subscribtion(
    body: Subscribtion,
    auth: dict = Depends(JWTBearer()),
    service: AdminService = Depends(get_service),
):
    entry_id = await service.add_subscription(body)
    return JSONResponse(f"{body.title} subscription created. ID: {entry_id.subscribe_id}")


@router.get(
    "/transactions",
    response_model=List[Transaction],
    response_description="Пример получения списка транзакций.",
    summary="Получить список транзакций.",
    description="Получение списка транзакций с пагинацией.",
)
async def get_list_transactions(
    commons: CommonQueryParams = Depends(CommonQueryParams),
    # auth: dict = Depends(JWTBearer()),
    service: AdminService = Depends(get_service),
) -> Optional[List[Dict[str, Transaction]]]:
    transactions = await service.get_transactions(
        page_size=commons.page_size, page_number=commons.page_number
    )
    if not transactions:
        return JSONResponse("No transactions")
    transaction_objs = [
        Transaction(
            user_id=transaction["user_id"],
            transaction_id=transaction["transaction_id"],
            value=transaction["value"],
            provider=transaction["provider"],
            idempotency_key_ttl=transaction["idempotency_key_ttl"],
            idempotency_key=transaction["idempotency_key"],
            operate_status=transaction["operate_status"],
            payment_details=transaction["payment_details"],
            created_at=transaction["created_at"],
            updated_at=transaction["updated_at"],
        )
        for transaction in transactions
    ]
    return transaction_objs


@router.put(
    "/update/{sub_id}",
    response_model=None,
    response_description="Изменение плана подписки.",
    summary="Изменение тарифного плана подписки.",
    description="Изменение тарифного плана подписки.",
)
async def update_sub(
    body: Subscribtion,
    sub_id: UUID,
    # auth: dict = Depends(JWTBearer()),
    service: AdminService = Depends(get_service),
):
    result = await service.update_subscription(id=sub_id, data=body)
    response = {
        "Message": "Succesfully update subscription",
        "Users, who have auto-renewal turned off": [user for user in result],
    }
    return JSONResponse(response, 200)
