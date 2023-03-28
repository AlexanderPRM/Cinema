from abc import abstractmethod
from typing import Dict, List, Optional

from elasticsearch import AsyncElasticsearch

from storage.base import BaseStorage


class PersonBaseStorage(BaseStorage):
    @abstractmethod
    async def get_data_list(self, page_number: int, page_size: int) -> List[Optional[Dict]]:
        pass

    @abstractmethod
    async def get_data_by_id(self, id: str) -> Optional[Dict]:
        pass

    @abstractmethod
    async def search_data(self, query, page_number: int, page_size: int):
        pass


class PersonElasticStorage(PersonBaseStorage):
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def search_data(self, query, page_number, page_size):
        search_query = {"query_string": {"default_field": "full_name", "query": query}}
        docs = await self.elastic.search(
            index="persons",
            body={
                "_source": ["id", "full_name", "films"],
                "from": (page_number - 1) * page_size,
                "size": page_size,
                "query": search_query,
            },
            params={"filter_path": "hits.hits._source"},
        )
        if not docs:
            return None
        return [person["_source"] for person in docs["hits"]["hits"]]

    async def get_data_by_id(self, id: str) -> Optional[Dict]:
        doc = await self.elastic.get("persons", id)
        if not doc:
            return None
        return doc["_source"]

    async def get_data_list(self, page_number: int, page_size: int) -> List[Optional[Dict]]:
        docs = await self.elastic.search(
            index="persons",
            body={
                "from": (page_number - 1) * page_size,
                "size": page_size,
                "query": {"match_all": {}},
            },
        )
        if not docs:
            return None
        return [person["_source"] for person in docs["hits"]["hits"]]
