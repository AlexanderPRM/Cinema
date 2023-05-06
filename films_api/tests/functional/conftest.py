import asyncio

import backoff
import elasticsearch
import pytest
import requests
from aiohttp import web_response

pytest_plugins = [
    "fixtures.elastic",
    "fixtures.aiohttp",
]


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
    max_tries=1,
    max_time=6,
)
@pytest.fixture
def make_get_request(aiohttp_client) -> web_response.Response:
    @backoff.on_exception(
        backoff.expo,
        (
            requests.exceptions.ConnectionError,
            ConnectionRefusedError,
            elasticsearch.exceptions.ConnectionError,
        ),
        max_tries=1,
        max_time=6,
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
        max_tries=1,
        max_time=6,
    )
    async def inner(url, query_data, settings):
        url = settings.service_url + url + query_data
        response = await aiohttp_client.get(url)
        return response

    return inner
