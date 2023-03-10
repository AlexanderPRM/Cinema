from http import HTTPStatus
from typing import Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from services.film import FilmService, get_film_service

router = APIRouter()


class Film(BaseModel):
    id: str
    title: str
    imdb_rating: float


class FilmDetail(BaseModel):
    id: str
    title: str
    imdb_rating: float
    desription: Optional[str]
    genre: List[Optional[dict]]
    actors: List[Optional[dict]]
    writers: List[Optional[dict]]
    director: List[Optional[str]]


# Внедряем FilmService с помощью Depends(get_film_service)
@router.get(
    "/{film_id}",
    response_model=FilmDetail,
    response_description="Пример вернушегося фильма",
    summary="Фильм",
    description=("Получение одного фильма по ID"),
)
async def film_details(
    film_id: str, film_service: FilmService = Depends(get_film_service)
) -> FilmDetail:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Film Not Found")
    return FilmDetail(
        id=film.id,
        title=film.title,
        imdb_rating=film.imdb_rating,
        desription=film.description,
        genre=film.genre,
        actors=film.actors,
        writers=film.writers,
        director=film.director,
    )


@router.get(
    "",
    response_model=List[Optional[Dict[str, Film]]],
    response_description="Пример вернувшегося списка фильмов.",
    response_model_exclude=["description", "genre", "actors", "writers", "director"],
    summary="Список фильмов",
    description="Список фильмов с пагинацией, "
    "фильтрацией по жанрам и сортировкой по названию или рейтингу.",
)
async def films(
    film_service: FilmService = Depends(get_film_service),
    sort: str = "-imdb_rating",
    genre: Optional[UUID] = None,
    page_number: Optional[int] = 1,
    page_size: Optional[int] = 10,
) -> Optional[List[Dict[str, Film]]]:
    films = await film_service.get_films(sort, genre, page_number, page_size)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Films Not Found")
    return films
