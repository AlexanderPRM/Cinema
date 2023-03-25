from functools import lru_cache
from typing import Optional

from elasticsearch import NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import AsyncElastic, get_elastic
from db.redis_db import get_redis
from models.film import Person, PersonList

PERSON_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class PersonService:
    def __init__(self, redis: Redis, elastic: AsyncElastic):
        self.redis = redis
        self.elastic = elastic

    async def search_persons(self, query, page_number, page_size):
        search_query = {"query_string": {"default_field": "full_name", "query": query}}
        persons = await self.elastic.search(
            index="persons",
            body={
                "_source": ["id", "full_name", "films"],
                "from": page_number,
                "size": page_size,
                "query": search_query,
            },
            params={"filter_path": "hits.hits._source"},
        )
        if not persons:
            return None
        return persons["hits"]["hits"]

    async def get_data_by_id(self, *args, **kwargs):
        (params,) = args
        person_id = params.get("person_id")
        person_id = str(person_id)
        person = await self._person_from_cache(person_id)
        if not person:
            person = await self._person_from_elastic(person_id)
            if not person:
                return None
            await self._put_person_to_cache(person)
        return person

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
                params={"filter_path": "hits.hits._source"},
            )
        except NotFoundError:
            return []
        return [PersonList(**person["_source"]) for person in docs["hits"]["hits"]]

    async def _person_from_elastic(self, person_id: str) -> Optional[Person]:
        try:
            doc = await self.elastic.get("persons", person_id)
        except NotFoundError:
            return None
        return Person(**doc["_source"])

    async def _person_from_cache(self, person_id: str) -> Optional[Person]:
        data = await self.redis.get(f"person_{person_id}")
        if not data:
            return None
        person = Person.parse_raw(data)
        return person

    async def _put_person_to_cache(self, person: Person):
        self.redis.set(f"person_{person.id}", person.json(), PERSON_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_person_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElastic = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
