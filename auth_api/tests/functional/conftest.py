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
        url = settings.service_url + "/user/signup/"
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


@pytest.fixture
def create_jwt_superuser_token():
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
        payload = {
            "sub": "1234567890",
            "jti": str(uuid.uuid4()),
            "exp": datetime.utcnow() + expires_in,
            "role": "superuser",
        }
        token = jwt.encode(payload, settings.jwt_secret, algorithm="HS256")
        return token

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
def make_post_request_role(aiohttp_client) -> web_response.Response:
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
def make_put_request_role(aiohttp_client) -> web_response.Response:
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
        response = await aiohttp_client.put(
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
def make_get_request_role(aiohttp_client) -> web_response.Response:
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
def get_role_id_by_name(make_get_request_role):
    @backoff.on_exception(
        backoff.expo,
        (
            requests.exceptions.ConnectionError,
            ConnectionRefusedError,
        ),
        max_tries=50,
        max_time=60,
    )
    async def inner(role_name, settings, headers={"Content-Type": "application/json"}, cookies={}):
        response = await make_get_request_role("/role/", headers=headers, settings=settings)
        response_text = await response.text()
        response_data = json.loads(response_text)

        async def async_work():
            coros = [check_role(role) for role in response_data["roles"]]
            done, _ = await asyncio.wait(coros, return_when=asyncio.FIRST_COMPLETED)
            for task in done:
                role_id = task.result()
                if role_id:
                    return role_id

        async def check_role(role_):
            if role_name == role_["name"]:
                return role_["id"]
            return None

        task = asyncio.create_task(async_work())
        role_id = await task
        return role_id

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
def make_delete_request_role(aiohttp_client) -> web_response.Response:
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
        response = await aiohttp_client.delete(
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
def create_account(aiohttp_client) -> web_response.Response:
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
        settings, email=f"{str(uuid.uuid4().hex)[:10]}@mail.ru", password="strongpassword"
    ):
        url = settings.service_url + "/user/signup/"
        query_data = {"email": email, "password": password}
        headers = {"Content-Type": "application/json"}
        response = await aiohttp_client.post(url, headers=headers, data=json.dumps(query_data))
        response_text = await response.text()
        response_data = json.loads(response_text)
        user_id = response_data.get("id")
        user_tokens = response_data.get("tokens")
        return {"user_id": user_id, "email": email, "password": password, "tokens": user_tokens}

    return inner
