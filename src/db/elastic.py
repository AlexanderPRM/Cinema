from typing import Optional

from elasticsearch import AsyncElasticsearch

es: Optional[AsyncElasticsearch] = None


class AsyncElastic:
    def __init__(self, engine: AsyncElasticsearch) -> None:
        self.engine = engine

    async def get(self, index, pk, **kwargs):
        doc = await self.engine.get(index, pk, **kwargs)
        return doc

    async def search(self, index, body, params, **kwargs):
        docs = await self.engine.search(index=index, body=body, params=params, **kwargs)
        return docs


# Функция понадобится при внедрении зависимостей
async def get_elastic() -> AsyncElastic:
    return AsyncElastic(es)
