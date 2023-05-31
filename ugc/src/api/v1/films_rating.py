import logging
from http import HTTPStatus
from uuid import UUID

from core.jwt import JWTBearer
from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from services.films_rating import RatingService, get_rating_service

router = APIRouter()


class Rating(BaseModel):
    rating: int


@router.post(
    "/{film_id}",
    response_description="Добавление/изменение пользовательского рейтинга к фильму",
    summary="Рейтинг",
    status_code=HTTPStatus.CREATED,
)
async def update_movie_rating(
    film_id: UUID,
    rating: Rating = Body(...),
    auth: dict = Depends(JWTBearer()),
    rating_service: RatingService = Depends(get_rating_service),
):
    if not auth:
        return JSONResponse({"message": "Token Invalid"}, status_code=HTTPStatus.FORBIDDEN)
    if rating.rating < 1 or rating.rating > 10:
        return JSONResponse(
            {"message": "Rating must be in range 1 to 10"}, status_code=HTTPStatus.BAD_REQUEST
        )
    film_id = film_id.__str__()
    user_id = auth["user_id"]
    rating_service.update_rating(film_id=film_id, user_id=user_id, rating=rating.rating)
    resp = JSONResponse({"message": f"Successfully add rating {rating.rating} to film {film_id}"})
    logging.info(resp)
    return resp


@router.post(
    "/delete/{film_id}",
    response_description="Удаление пользовательского рейтинга",
    summary="Рейтинг",
    status_code=HTTPStatus.CREATED,
)
async def remove_movie_rating(
    film_id: UUID,
    auth: dict = Depends(JWTBearer()),
    rating_service: RatingService = Depends(get_rating_service),
):
    if not auth:
        return JSONResponse({"message": "Token Invalid"}, status_code=HTTPStatus.FORBIDDEN)
    film_id = film_id.__str__()
    user_id = auth["user_id"]
    check = rating_service.check_rating_exists(film_id=film_id, user_id=user_id)
    if not check:
        return JSONResponse(
            {"message": "The user has not yet rated this movie"}, status_code=HTTPStatus.BAD_REQUEST
        )
    rating_service.delete_rating(film_id=film_id, user_id=user_id)
    resp = JSONResponse({"message": f"Successfully remove rating from film {film_id}"})
    logging.info(resp)
    return resp
