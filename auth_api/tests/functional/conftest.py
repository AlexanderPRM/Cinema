import asyncio
import json
import uuid
from email import header

import backoff
import pytest
import requests
from aiohttp import web_response

pytest_plugins = [
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
    ),
    max_tries=50,
    max_time=60,
)
@pytest.fixture
def make_post_request(aiohttp_client) -> web_response.Response:
    @backoff.on_exception(
        backoff.expo,
        (
            requests.exceptions.ConnectionError,
            ConnectionRefusedError,
        ),
        max_tries=50,
        max_time=60,
    )
    async def inner(url, settings, query_data={}, cookies={}):
        url = settings.service_url + url
        query_data = query_data
        headers = {"Content-Type": "application/json"}
        response = await aiohttp_client.post(
            url, headers=headers, data=json.dumps(query_data), cookies=cookies
        )
        return response

    return inner


@backoff.on_exception(
    backoff.expo,
    (
        requests.exceptions.ConnectionError,
        ConnectionRefusedError,
    ),
    max_tries=50,
    max_time=60,
)
@pytest.fixture
def make_get_request(aiohttp_client) -> web_response.Response:
    @backoff.on_exception(
        backoff.expo,
        (
            requests.exceptions.ConnectionError,
            ConnectionRefusedError,
        ),
        max_tries=50,
        max_time=60,
    )
    async def inner(url, settings, query_data={}, cookies={}):
        url = settings.service_url + url
        query_data = query_data
        headers = {"Content-Type": "application/json"}
        response = await aiohttp_client.get(
            url, headers=headers, data=json.dumps(query_data), cookies=cookies
        )
        return response

    return inner


@backoff.on_exception(
    backoff.expo,
    (
        requests.exceptions.ConnectionError,
        ConnectionRefusedError,
    ),
    max_tries=50,
    max_time=60,
)
@pytest.fixture
def get_access_token(aiohttp_client) -> web_response.Response:
    @backoff.on_exception(
        backoff.expo,
        (
            requests.exceptions.ConnectionError,
            ConnectionRefusedError,
        ),
        max_tries=50,
        max_time=60,
    )
    async def inner(settings, email=f"{str(uuid.uuid4().hex)[:10]}@mail.ru"):
        password = "1"
        url = settings.service_url + "/user/signup"
        query_data = {"email": email, "password": password, "name": "Romel"}
        headers = {"Content-Type": "application/json"}
        response = await aiohttp_client.post(url, headers=headers, data=json.dumps(query_data))
        response_text = await response.text()
        response_data = json.loads(response_text)
        access_token = response_data.get("tokens").get("access_token")
        return access_token

    return inner


@pytest.fixture
def make_get_request_id(aiohttp_client):
    @backoff.on_exception(
        backoff.expo,
        (
            requests.exceptions.ConnectionError,
            ConnectionRefusedError,
        ),
        max_tries=50,
        max_time=60,
    )
    async def inner(url, query_data, settings):
        url = settings.service_url + url
        response = await aiohttp_client.get(url, params=query_data)
        return response

    return inner
