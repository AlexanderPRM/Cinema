import logging
from datetime import datetime
from http import HTTPStatus
from uuid import UUID

from core.config import collections_names
from core.jwt import JWTBearer
from db.mongo import Mongo, get_db
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from models.review import Review
from pydantic import BaseModel
from services.films_reviews import ReviewService, get_review_service

router = APIRouter()


class FilmReview(BaseModel):
    text: str


@router.post(
    "/{film_id}",
    response_description="Добавление рецензии к фильму",
    summary="Рецензия",
    status_code=HTTPStatus.CREATED,
)
async def film_review(
    film_id: UUID,
    body: FilmReview,
    auth: dict = Depends(JWTBearer()),
    mongodb: Mongo = Depends(get_db),
):
    if not auth:
        return JSONResponse({"message": "Token Invalid"}, status_code=HTTPStatus.FORBIDDEN)
    collection = mongodb.get_collection(collections_names.FILM_REVIEW_COLLECTION)
    doc = {
        "film_id": film_id.__str__(),
        "author": auth["user_id"],
        "text": body.text,
        "created_at": datetime.now(),
    }
    query_res = collection.insert_one(doc)
    logging.info(f"Successfully insert film review {query_res.inserted_id}")
    return {"message": "Success"}


@router.get(
    "/",
    response_description="Получение списка рецензий всех пользователей ко всем фильмам",
    summary="Рецензия",
    status_code=HTTPStatus.OK,
)
async def film_get_reviews(
    review_service: ReviewService = Depends(get_review_service),
    auth: dict = Depends(JWTBearer()),
    sort_direction: str = "desc",  # desc / asc
    page_number: int = 1,
    page_size: int = 5,
):
    if not auth:
        return JSONResponse({"message": "Token Invalid"}, status_code=HTTPStatus.FORBIDDEN)
    if page_number < 1 or page_size < 1:
        return JSONResponse(
            {"message": "Invalid request parameters"}, status_code=HTTPStatus.BAD_REQUEST
        )
    if sort_direction not in ("desc", "asc"):
        return JSONResponse(
            {"message": "Parameter sort_direction must be 'desc' or 'asc' or None"},
            status_code=HTTPStatus.BAD_REQUEST,
        )
    reviews = review_service.get_reviews_list(
        sort_direction=sort_direction, page_number=page_number, page_size=page_size
    )
    response = [
        Review(
            id=str(review["_id"]),
            film_id=review["film_id"],
            author=review["author"],
            text=review["text"],
            created_at=str(review["created_at"]),
        )
        for review in reviews
    ]
    return {"reviews": response}
