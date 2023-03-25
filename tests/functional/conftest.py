import asyncio
import json

import aiohttp
import pytest
import pytest_asyncio
from aiohttp import web_response
from elasticsearch import AsyncElasticsearch

from . import settings
from .settings import films_settings


def get_es_bulk_query(es_data: list[dict], es_index: str, es_id_field: str) -> list:
    bulk_query = []
    for row in es_data:
        bulk_query.extend(
            [json.dumps({"index": {"_index": es_index, "_id": row[es_id_field]}}), json.dumps(row)]
        )
    print(bulk_query)
    return bulk_query


@pytest.fixture(scope="session")
def event_loop():
    """Overrides pytest default function scoped event loop"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def es_client():
    client = AsyncElasticsearch(hosts=films_settings.es_adress, validate_cert=False, use_ssl=False)
    yield client
    await client.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def aiohttp_client():
    client = aiohttp.ClientSession()
    yield client
    await client.close()


@pytest.fixture
def es_write_films_data(es_client):
    async def inner(data: list[dict]) -> None:
        bulk_query = get_es_bulk_query(data, films_settings.es_index, films_settings.es_id_field)
        str_query = "\n".join(bulk_query) + "\n"
        response = await es_client.bulk(str_query, refresh=True)
        if response["errors"]:
            raise Exception("Ошибка записи данных в Elasticsearch")

    return inner


@pytest.fixture
def make_get_request(aiohttp_client) -> web_response.Response:
    async def inner(url, query_data):
        url = settings.films_settings.service_url + url
        query_data = query_data
        response = await aiohttp_client.get(url, params=query_data)
        return response

    return inner
