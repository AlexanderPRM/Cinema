from functools import lru_cache
from typing import Dict, List, Optional
from uuid import UUID

from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from redis.asyncio import Redis

from cache.base import BaseCache
from cache.redis_cache import RedisCache
from db.elastic import get_elastic
from db.redis_db import get_redis
from storage.films import FilmBaseStorage, FilmElasticStorage

# from models.film import Film, FilmDetail


class FilmService:

    def __init__(self, cache: BaseCache, storage: FilmBaseStorage):
        self.cache = cache
        self.storage = storage

    async def search_data(self, query, page_number: int, page_size: int):
        data = await self.storage.search_data(query, page_number=page_number, page_size=page_size)
        return data

    async def get_data_by_id(self, url: str, id: str) -> Optional[Dict]:
        data = await self.cache.get_object_from_cache(url)
        if not data:
            data = await self.storage.get_data_by_id(id=id)
            if data:
                await self.cache.put_object_to_cache(url, data)

        return data

    async def get_data_list(
            self, sort:
            str, genre:
            UUID, page_number:
            int,
            page_size: int
    ) -> Optional[List[Dict]]:
        data = await self.storage.get_data_list(
            sort=sort,
            genre=genre,
            page_number=page_number,
            page_size=page_size
        )
        return data


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    redis = RedisCache(redis)
    elastic = FilmElasticStorage(elastic)
    return FilmService(redis, elastic)
