import logging
from datetime import datetime
from http import HTTPStatus
from uuid import UUID

from core.config import collections_names
from core.jwt import JWTBearer
from db.mongo import Mongo, get_db
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel

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
    logging.info(f"Succesfully insert film review {query_res.inserted_id}")
    return {"message": "Success"}
