from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request

from models.film import Genre
from services.genres import GenreService, get_genre_service

router = APIRouter()


@router.get(
    "/{genre_id}",
    response_model=Genre,
    description="Получить информацию о жанре",
    response_description="Подробная информация о жанре",
)
async def genre_details(
    request: Request, genre_id: str, genre_service: GenreService = Depends(get_genre_service)
) -> Genre:
    query_params = dict(genre_id=genre_id, request=request, index="genres")
    genre = await genre_service.get_data_by_id(query_params)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return Genre(id=genre.id, name=genre.name)


@router.get(
    "/",
    response_model=list[Genre],
    description="Список жанров",
    response_description="Список жанров",
)
async def list_genres(
    request: Request,
    genre_service: GenreService = Depends(get_genre_service),
    page_number=1,
    page_size=20,
) -> list[Genre]:
    query_params = dict(
        request=request,
        index="genres",
        page_number=page_number,
        page_size=page_size,
    )
    genres = await genre_service.get_data_list(query_params)
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return [Genre(id=genre.id, name=genre.name) for genre in genres]