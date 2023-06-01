from http import HTTPStatus
from uuid import UUID

from core.jwt import JWTBearer
from db.mongo import Mongo, get_db
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from services.bookmarks import BookmarksService

router = APIRouter()


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
    if not auth:
        return JSONResponse({"message": "Token Invalid"}, status_code=HTTPStatus.FORBIDDEN)
    BookmarksService.post_bookmark(mongodb=mongodb, user_id=auth["user_id"], film_id=str(film_id))
    return {"message": "Success"}


@router.delete(
    "/{film_id}/",
    response_description="Удаление фильма из закладок",
    status_code=HTTPStatus.OK
)
async def delete_bookmark(
    film_id: UUID,
    auth: dict = Depends(JWTBearer()),
    mongodb: Mongo = Depends(get_db),
):
    if not auth:
        return JSONResponse({"message": "Token Invalid"}, status_code=HTTPStatus.FORBIDDEN)
    BookmarksService.delete_bookmark(mongodb=mongodb, user_id=auth["user_id"], film_id=str(film_id))
    return {"message": "Success"}
