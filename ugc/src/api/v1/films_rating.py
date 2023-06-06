import logging
from http import HTTPStatus
from uuid import UUID

from core.jwt import JWTBearer
from core.logging_setup import LOGGER
from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from services.films_rating import RatingService, get_rating_service

router = APIRouter()


@router.post(
    "/{film_id}",
    response_description="Добавление/изменение пользовательского рейтинга к фильму",
    summary="Рейтинг",
    status_code=HTTPStatus.CREATED,
)
async def update_movie_rating(
    film_id: UUID,
    rating: int = Body(embed=True, ge=1, lt=11),
    auth: dict = Depends(JWTBearer()),
    rating_service: RatingService = Depends(get_rating_service),
):
    film_id = film_id.__str__()
    user_id = auth["user_id"]
    rating_service.update_rating(film_id=film_id, user_id=user_id, rating=rating)
    resp = JSONResponse({"message": f"Successfully add rating {rating} to film {film_id}"})
    LOGGER.info(resp)
    return resp


@router.delete(
    "/delete/{film_id}",
    response_description="Удаление пользовательского рейтинга",
    summary="Рейтинг",
    status_code=HTTPStatus.NO_CONTENT,
)
async def remove_movie_rating(
    film_id: UUID,
    auth: dict = Depends(JWTBearer()),
    rating_service: RatingService = Depends(get_rating_service),
):
    film_id = film_id.__str__()
    user_id = auth["user_id"]
    check = rating_service.check_rating_exists(film_id=film_id, user_id=user_id)
    if not check:
        return JSONResponse(
            {"message": "The user has not yet rated this movie"}, status_code=HTTPStatus.BAD_REQUEST
        )
    rating_service.delete_rating(film_id=film_id, user_id=user_id)
    resp = JSONResponse({"message": f"Successfully remove rating from film {film_id}"})
    LOGGER.info(resp)
    return resp


@router.get(
    "/{film_id}",
    response_description="Просмотр среднего пользовательского рейтинга фильма",
    summary="Рейтинг",
    status_code=HTTPStatus.OK,
)
async def get_movie_rating(
    film_id: UUID,
    auth: dict = Depends(JWTBearer()),
    rating_service: RatingService = Depends(get_rating_service),
):
    film_id = film_id.__str__()
    rating = rating_service.get_average_rating(film_id=film_id)
    if rating == 0:
        return JSONResponse({"message": f"No one has rated movie {film_id} yet"})
    resp = JSONResponse({"Film": film_id, "Rating": rating})
    LOGGER.info(resp)
    return resp


@router.get(
    "summary/{film_id}",
    response_description="Получить кол-во оценок фильма",
    status_code=HTTPStatus.OK,
)
async def film_like_count(
    film_id: UUID,
    auth: dict = Depends(JWTBearer()),
    rating_service: RatingService = Depends(get_rating_service),
):
    query_res = rating_service.count_likes_quantity(film_id=(str(film_id)))
    return {"quantity": query_res}
