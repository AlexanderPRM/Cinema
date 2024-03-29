from http import HTTPStatus
from uuid import UUID

from core.config import CommonQueryParams
from fastapi import APIRouter, Depends, HTTPException, Request
from models.film import Genre
from services.base import verify_jwt
from services.genres import GenreService, get_genre_service

router = APIRouter()


@router.get(
    "/{genre_id}",
    response_model=Genre,
    summary="Жанр",
    description="Получить информацию о жанре",
    response_description="Подробная информация о жанре",
)
async def genre_details(
    request: Request, genre_id: UUID, genre_service: GenreService = Depends(get_genre_service)
) -> Genre:
    await verify_jwt(request)
    genre = await genre_service.get_data_by_id(url=str(request.url), id=str(genre_id))
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return Genre(
        id=genre["id"],
        name=genre["name"],
    )


@router.get(
    "/",
    response_model=list[Genre],
    description="Список жанров с пагинацией",
    summary="Список жанров",
    response_description="Список жанров",
)
async def list_genres(
    request: Request,
    genre_service: GenreService = Depends(get_genre_service),
    commons: CommonQueryParams = Depends(CommonQueryParams),
) -> list[Genre]:
    await verify_jwt(request)
    genres = await genre_service.get_data_list(
        page_number=commons.page_number, page_size=commons.page_size
    )
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return [
        Genre(
            id=genre["id"],
            name=genre["name"],
        )
        for genre in genres
    ]
