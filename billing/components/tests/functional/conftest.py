import asyncio
import json
import uuid
from datetime import datetime, timedelta, timezone

import backoff
import jwt
import pytest
import requests
from aiohttp import client_exceptions, web_response

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
    async def inner(settings, user_uuid: str = str(uuid.uuid4())):
        expires_in = timedelta(days=1)
        now = datetime.now(timezone.utc)
        payload = {
            "user_id": str(uuid.uuid4()),
            "fresh": True,
            "nbf": now,
            "type": "access",
            "csrf": str(uuid.uuid4()),
            "sub": "admin",
            "jti": str(uuid.uuid4()),
            "exp": datetime.utcnow() + expires_in,
            "role": "superuser",
        }
        token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
        return token, user_uuid

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
        url = settings.service_url + "/user/signup/"
        query_data = {"email": email, "password": password, "name": "Romel"}
        headers = {"Content-Type": "application/json"}
        response = await aiohttp_client.post(url, headers=headers, data=json.dumps(query_data))
        response_text = await response.text()
        response_data = json.loads(response_text)
        access_token = response_data.get("tokens").get("access_token")
        return access_token

    return inner


@backoff.on_exception(
    backoff.expo,
    (
        requests.exceptions.ConnectionError,
        ConnectionRefusedError,
        client_exceptions.ServerDisconnectedError,
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
            client_exceptions.ServerDisconnectedError,
        ),
        max_tries=50,
        max_time=60,
    )
    async def inner(
        url, settings, headers={"content-type": "application/json"}, query_data={}, cookies={}
    ):
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
        client_exceptions.ServerDisconnectedError,
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
            client_exceptions.ServerDisconnectedError,
        ),
        max_tries=50,
        max_time=60,
    )
    async def inner(
        url,
        settings,
        headers={"Content-Type": "application/json"},
        query_data={},
        cookies={},
        params={},
    ):
        response = await aiohttp_client.get(
            url, headers=headers, data=json.dumps(query_data), cookies=cookies, params=params
        )
        return response

    return inner


@backoff.on_exception(
    backoff.expo,
    (
        requests.exceptions.ConnectionError,
        ConnectionRefusedError,
        client_exceptions.ServerDisconnectedError,
    ),
    max_tries=50,
    max_time=60,
)
@pytest.fixture
def make_put_request(aiohttp_client) -> web_response.Response:
    @backoff.on_exception(
        backoff.expo,
        (
            requests.exceptions.ConnectionError,
            ConnectionRefusedError,
            client_exceptions.ServerDisconnectedError,
        ),
        max_tries=50,
        max_time=60,
    )
    async def inner(
        url,
        settings,
        headers={"Content-Type": "application/json"},
        query_data={},
        cookies={},
        params={},
    ):
        response = await aiohttp_client.put(
            url, headers=headers, data=json.dumps(query_data), cookies=cookies, params=params
        )
        return response

    return inner
