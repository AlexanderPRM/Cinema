from http import HTTPStatus
from typing import Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request

from core.config import CommonQueryParams
from models.film import Film, FilmDetail
from services.film import FilmService, get_film_service

router = APIRouter()


@router.get(
    "",
    response_model=List[Film],
    response_description="Пример вернувшегося списка фильмов.",
    response_model_exclude={"description", "genre", "actors", "writers", "director"},
    summary="Список фильмов",
    description="Список фильмов с пагинацией, "
    "фильтрацией по жанрам и сортировкой по названию или рейтингу.",
)
async def films(
    film_service: FilmService = Depends(get_film_service),
    sort: str = "-imdb_rating",
    genre: Optional[UUID] = None,
    commons: CommonQueryParams = Depends(CommonQueryParams),
) -> Optional[List[Dict[str, Film]]]:
    films = await film_service.get_data_list(sort, genre, commons.page_number, commons.page_size)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Films Not Found")
    return films


@router.get(
    "/search",
    response_model=List[Film],
    response_description="Пример найденных фильмов",
    response_model_exclude={"description", "genre", "actors", "writers", "director"},
    description="Полнотекстовый поиск по фильмам",
    summary="Список найденных фильмов",
)
async def search_films(
    film_service: FilmService = Depends(get_film_service),
    query: str = "",
    commons: CommonQueryParams = Depends(CommonQueryParams),
) -> Optional[List[Dict[str, Film]]]:
    films = await film_service.search_data(query, commons.page_number, commons.page_size)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Films Not Found")
    return films


# Внедряем FilmService с помощью Depends(get_film_service)
@router.get(
    "/{film_id}",
    response_model=FilmDetail,
    response_description="Пример вернушегося фильма",
    summary="Фильм",
    description=("Получение одного фильма по ID"),
)
async def film_details(
    request: Request,
    film_id: UUID,
    film_service: FilmService = Depends(get_film_service)
) -> FilmDetail:
    film = await film_service.get_data_by_id(url=str(request.url), id=str(film_id))
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Film Not Found")
    return film
