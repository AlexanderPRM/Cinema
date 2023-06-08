from http import HTTPStatus
from uuid import UUID

from core.jwt import JWTBearer
from core.logging_setup import LOGGER
from db.mongo import Mongo, get_db
from fastapi import APIRouter, Depends
from services.bookmarks import BookmarksService

router = APIRouter()


@router.get(
    "/",
    response_description="Получение фильмов из закладок",
    status_code=HTTPStatus.OK,
)
async def get_bookmarks(
    auth: dict = Depends(JWTBearer()),
    mongodb: Mongo = Depends(get_db),
):
    query_res = await BookmarksService.get_bookmarks(mongodb=mongodb, user_id=auth["user_id"])

    return {"message": "Success", "user_id": auth["user_id"], "data": query_res}


@router.post(
    "/{film_id}/",
    response_description="Добавление фильма в закладки",
    status_code=HTTPStatus.CREATED,
)
async def create_bookmark(
    film_id: UUID,
    auth: dict = Depends(JWTBearer()),
    mongodb: Mongo = Depends(get_db),
):
    query_res = await BookmarksService.post_bookmark(
        mongodb=mongodb, user_id=auth["user_id"], film_id=str(film_id)
    )
    LOGGER.info(f"Add bookmark | film_id: {film_id}")
    return {"message": "Success", "_id": str(query_res.inserted_id)}


@router.delete(
    "/{film_id}/", response_description="Удаление фильма из закладок", status_code=HTTPStatus.OK
)
async def delete_bookmark(
    film_id: UUID,
    auth: dict = Depends(JWTBearer()),
    mongodb: Mongo = Depends(get_db),
):
    query_res = await BookmarksService.delete_bookmark(
        mongodb=mongodb, user_id=auth["user_id"], film_id=str(film_id)
    )
    return {"message": "Success", "_id": str(query_res.inserted_id)}
