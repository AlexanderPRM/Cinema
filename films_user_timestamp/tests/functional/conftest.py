import asyncio
import json
import uuid
from datetime import datetime, timedelta

import backoff
import jwt
import pytest
import requests
from aiohttp import web_response

pytest_plugins = [
    "client.aiohttp",
]


@pytest.fixture(scope="session")
def event_loop():
    """Overrides pytest default function scoped event loop."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def get_jwt_token():
    @backoff.on_exception(
        backoff.expo,
        (
            requests.exceptions.ConnectionError,
            ConnectionRefusedError,
        ),
        max_tries=50,
        max_time=60,
    )
    async def inner(settings):
        expires_in = timedelta(days=1)
        user_id = str(uuid.uuid4())
        payload = {
            "sub": "1234567890",
            "jti": str(uuid.uuid4()),
            "exp": datetime.utcnow() + expires_in,
            "role": "test",
            "user_id": user_id,
        }
        token = jwt.encode(payload, settings.jwt_secret, algorithm="HS256")
        return token, user_id

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
    async def inner(
        url, settings, headers={"Content-Type": "application/json"}, query_data={}, cookies={}
    ):
        url = settings.service_url + url
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
    async def inner(
        url, settings, headers={"Content-Type": "application/json"}, query_data={}, cookies={}
    ):
        url = settings.service_url + url
        response = await aiohttp_client.get(
            url, headers=headers, data=json.dumps(query_data), cookies=cookies
        )
        return response

    return inner
