from abc import abstractmethod
from typing import Dict, List, Optional

from elasticsearch import AsyncElasticsearch, exceptions

from storage.base import BaseStorage


class GenreBaseStorage(BaseStorage):
    @abstractmethod
    async def get_data_list(self, page_number: int, page_size: int) -> List[Optional[Dict]]:
        pass

    @abstractmethod
    async def get_data_by_id(self, id: str) -> Optional[Dict]:
        pass


class GenreElasticStorage(GenreBaseStorage):
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get_data_by_id(self, id: str) -> Optional[Dict]:
        try:
            doc = await self.elastic.get("genres", id)
            return doc["_source"]
        except exceptions.NotFoundError:
            return None

    async def get_data_list(self, page_number: int, page_size: int) -> List[Optional[Dict]]:
        try:
            docs = await self.elastic.search(
                index="genres",
                body={
                    "from": page_number,
                    "size": page_size,
                    "query": {"match_all": {}},
                },
            )
            return [genre["_source"] for genre in docs["hits"]["hits"]]
        except exceptions.NotFoundError:
            return None
