from functools import lru_cache
from typing import Optional

from elasticsearch import NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import AsyncElastic, get_elastic
from db.redis_db import get_redis
from models.film import Genre

GENRE_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class GenreService:
    def __init__(self, redis: Redis, elastic: AsyncElastic):
        self.redis = redis
        self.elastic = elastic

    async def get_data_by_id(self, *args, **kwargs):
        (params,) = args
        genre_id = params.get("genre_id")
        genre_id = str(genre_id)
        genre = await self._genre_from_cache(genre_id)
        if not genre:
            genre = await self._genre_from_elastic(genre_id)
            if not genre:
                return None
            await self._put_genre_to_cache(genre)
        return genre

    async def get_data_list(self, *args, **kwargs):
        (params,) = args
        try:
            docs = await self.elastic.search(
                index=params.get("index"),
                body={
                    "from": params.get("page_number"),
                    "size": params.get("page_size"),
                    "query": {"match_all": {}},
                },
            )
        except NotFoundError:
            return []
        return [Genre(**genre["_source"]) for genre in docs["hits"]["hits"]]

    async def _genre_from_elastic(self, genre_id: str) -> Optional[Genre]:
        try:
            doc = await self.elastic.get("genres", genre_id)
        except NotFoundError:
            return None
        return Genre(**doc["_source"])

    async def _genre_from_cache(self, genre_id: str) -> Optional[Genre]:
        data = await self.redis.get(f"genre_{genre_id}")
        if not data:
            return None
        genre = Genre.parse_raw(data)
        return genre

    async def _put_genre_to_cache(self, genre: Genre):
        self.redis.set(f"genre_{genre.id}", genre.json(), GENRE_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElastic = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
