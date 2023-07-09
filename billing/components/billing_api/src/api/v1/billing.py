from fastapi import APIRouter
from models.billing import Pay

router = APIRouter()


@router.post(
    "/pay/{subscribe_plan_id}/",
    response_model=None,
    response_description="Пример информации о платежа с ссылкой для оплаты.",
    summary="Оплата подписки.",
    description="Оплата подписки по какому-то выбранному плану.",
)
async def pay(body: Pay):
    pass
