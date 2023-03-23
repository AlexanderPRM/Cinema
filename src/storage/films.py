from abc import abstractmethod
from typing import Dict, List, Optional
from uuid import UUID

from elasticsearch import AsyncElasticsearch

from storage.base import BaseStorage


class FilmBaseStorage(BaseStorage):
    @abstractmethod
    async def get_data_list(self, page_number: int, page_size: int) -> List[Optional[Dict]]:
        pass

    @abstractmethod
    async def get_data_by_id(self, id: str) -> Optional[Dict]:
        pass

    @abstractmethod
    async def search_data(self, query, page_number: int, page_size: int):
        pass


class FilmElasticStorage(FilmBaseStorage):
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def search_data(self, query, page_number, page_size):
        search_query = {"query_string": {"default_field": "title", "query": query}}
        docs = await self.elastic.search(
            index="movies",
            body={
                "_source": ["id", "title", "imdb_rating"],
                "from": page_number,
                "size": page_size,
                "query": search_query,
            },
            params={"filter_path": "hits.hits._source"},
        )
        if not docs:
            return None
        return [film["_source"] for film in docs["hits"]["hits"]]

    async def get_data_by_id(self, id: str) -> Optional[Dict]:
        doc = await self.elastic.get("movies", id)
        if not doc:
            return None
        return doc["_source"]

    async def get_data_list(
            self,
            sort: str,
            genre: UUID,
            page_number: int,
            page_size: int
    ) -> List[Optional[Dict]]:
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
        docs = await self.elastic.search(
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
        if not docs:
            return None
        return [film["_source"] for film in docs["hits"]["hits"]]
