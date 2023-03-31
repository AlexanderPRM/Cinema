import asyncio
import json

import aiohttp
import backoff
import elasticsearch
import pytest
import pytest_asyncio
import requests
from aiohttp import web_response
from elasticsearch import AsyncElasticsearch

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
    """Overrides pytest default function scoped event loop."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@backoff.on_exception(
    backoff.expo,
    (
        requests.exceptions.ConnectionError,
        ConnectionRefusedError,
        elasticsearch.exceptions.ConnectionError,
    ),
    max_tries=50,
    max_time=60,
)
@pytest_asyncio.fixture(scope="session", autouse=True)
async def es_client():
    client = AsyncElasticsearch(hosts=films_settings.es_adress, validate_cert=False, use_ssl=False)
    yield client
    await client.close()


@backoff.on_exception(
    backoff.expo,
    (
        requests.exceptions.ConnectionError,
        ConnectionRefusedError,
        aiohttp.client_exceptions.ClientConnectorError,
    ),
    max_tries=50,
    max_time=60,
)
@pytest_asyncio.fixture(scope="session", autouse=True)
async def aiohttp_client():
    client = aiohttp.ClientSession()
    yield client
    await client.close()


@pytest.fixture
def es_write_data(es_client):
    @backoff.on_exception(
        backoff.expo,
        (
            requests.exceptions.ConnectionError,
            ConnectionRefusedError,
            elasticsearch.exceptions.ConnectionError,
        ),
        max_tries=50,
        max_time=60,
    )
    async def inner(data: list[dict], settings) -> None:
        bulk_query = get_es_bulk_query(data, settings.es_index, settings.es_id_field)
        str_query = "\n".join(bulk_query) + "\n"
        response = await es_client.bulk(str_query, refresh=True)
        if response["errors"]:
            raise Exception("Ошибка записи данных в Elasticsearch")

    return inner


@pytest.fixture
def make_get_request(aiohttp_client) -> web_response.Response:
    @backoff.on_exception(
        backoff.expo,
        (
            requests.exceptions.ConnectionError,
            ConnectionRefusedError,
            elasticsearch.exceptions.ConnectionError,
        ),
        max_tries=50,
        max_time=60,
    )
    async def inner(url, settings, query_data={}):
        url = settings.service_url + url
        query_data = query_data
        response = await aiohttp_client.get(url, params=query_data)
        return response

    return inner


@pytest.fixture
def make_get_request_id(aiohttp_client):
    @backoff.on_exception(
        backoff.expo,
        (
            requests.exceptions.ConnectionError,
            ConnectionRefusedError,
            elasticsearch.exceptions.ConnectionError,
        ),
        max_tries=50,
        max_time=60,
    )
    async def inner(url, query_data, settings):
        url = settings.service_url + url + query_data
        response = await aiohttp_client.get(url)
        return response

    return inner


@pytest.fixture
def es_clear_data(es_client):
    @backoff.on_exception(
        backoff.expo,
        (
            requests.exceptions.ConnectionError,
            ConnectionRefusedError,
            elasticsearch.exceptions.ConnectionError,
        ),
        max_tries=50,
        max_time=60,
    )
    async def inner(index):
        await es_client.delete_by_query(index=index, body={"query": {"match_all": {}}})

    return inner
