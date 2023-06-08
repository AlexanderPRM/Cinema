from http import HTTPStatus
from uuid import UUID

from core.jwt import JWTBearer
from fastapi import APIRouter, Depends
from services.films_rating import RatingService, get_rating_service

router = APIRouter()


@router.get(
    "/{film_id}",
    response_description="Получить кол-во оценок фильма",
    status_code=HTTPStatus.OK,
)
async def film_like_count(
    film_id: UUID,
    auth: dict = Depends(JWTBearer()),
    rating_service: RatingService = Depends(get_rating_service),
):
    query_res = await rating_service.count_likes_quantity(film_id=(str(film_id)))
    return {"quantity": query_res}
