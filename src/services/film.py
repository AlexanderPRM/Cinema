from functools import lru_cache
from typing import List, Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis_db import get_redis
from models.film import FilmDetail

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def search_films(self, query, page_number, page_size) -> Optional[List[FilmDetail]]:
        search_query = {"query_string": {"default_field": "title", "query": query}}
        films = await self.elastic.search(
            index="movies",
            body={
                "_source": ["id", "title", "imdb_rating"],
                "from": page_number,
                "size": page_size,
                "query": search_query,
            },
            params={"filter_path": "hits.hits._source"},
        )
        if not films:
            return None
        return films["hits"]["hits"]

    async def get_films(self, sort, genre, page_number, page_size) -> Optional[List[FilmDetail]]:
        if sort[0] == "-":
            sort = {sort[1:]: "desc"}
        else:
            sort = {sort: "asc"}
        filter_query = (
            {"match_all": {}}
            if genre is None
            else {
                "nested": {
                    "path": "genre",
                    "query": {"bool": {"must": {"match": {"genre.id": genre}}}},
                }
            }
        )
        films = await self.elastic.search(
            index="movies",
            body={
                "_source": ["id", "title", "imdb_rating"],
                "sort": sort,
                "from": page_number,
                "size": page_size,
                "query": filter_query,
            },
            params={"filter_path": "hits.hits._source"},
        )
        if not films:
            return None
        return films["hits"]["hits"]

    # get_by_id возвращает объект фильма. Он опционален, так как фильм может отсутствовать в базе
    async def get_by_id(self, film_id: str) -> Optional[FilmDetail]:
        # Пытаемся получить данные из кеша, потому что оно работает быстрее
        film = await self._film_from_cache(film_id)
        if not film:
            # Если фильма нет в кеше, то ищем его в Elasticsearch
            film = await self._get_film_from_elastic(film_id)
            if not film:
                # Если он отсутствует в Elasticsearch, значит, фильма вообще нет в базе
                return None
            # Сохраняем фильм  в кеш
            await self._put_film_to_cache(film)

        return film

    async def _get_film_from_elastic(self, film_id: str) -> Optional[FilmDetail]:
        try:
            doc = await self.elastic.get("movies", film_id)
        except NotFoundError:
            return None
        return FilmDetail(**doc["_source"])

    async def _film_from_cache(self, film_id: str) -> Optional[FilmDetail]:
        # Пытаемся получить данные о фильме из кеша, используя команду get
        # https://redis.io/commands/get/
        data = await self.redis.get(film_id)
        if not data:
            return None

        # pydantic предоставляет удобное API для создания объекта моделей из json
        film = FilmDetail.parse_raw(data)
        return film

    async def _put_film_to_cache(self, film: FilmDetail):
        # Сохраняем данные о фильме, используя команду set
        # Выставляем время жизни кеша — 5 минут
        # https://redis.io/commands/set/
        # pydantic позволяет сериализовать модель в json
        await self.redis.set(film.id, film.json(), FILM_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
