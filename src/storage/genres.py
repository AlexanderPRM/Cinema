from abc import abstractmethod
from typing import Dict, List, Optional

from elasticsearch import AsyncElasticsearch

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
        doc = await self.elastic.get("genres", id)
        if not doc:
            return None
        return doc["_source"]

    async def get_data_list(self, page_number: int, page_size: int) -> List[Optional[Dict]]:
        docs = await self.elastic.search(
            index="genres",
            body={
                "from": (page_number - 1) * page_size,
                "size": page_size,
                "query": {"match_all": {}},
            },
        )
        if not docs:
            return None
        return [genre["_source"] for genre in docs["hits"]["hits"]]
