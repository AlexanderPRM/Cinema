import datetime
import json
import uuid
from http import HTTPStatus

import pytest
from pytest import fixture
from settings import baseconfig

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "expected_status, expected_message, expected_timestamp",
    [
        (HTTPStatus.CREATED, "OK", str(datetime.datetime.now().replace(second=0, microsecond=0))),
    ],
)
async def test_post_film_timestamp(
    get_jwt_token: fixture,
    make_post_request: fixture,
    expected_status: int,
    expected_message: str,
    expected_timestamp: str,
):
    token, _ = await get_jwt_token(settings=baseconfig)
    headers = {"Authorization": f"Bearer {token}", "content-type": "application/json"}
    film_id = uuid.uuid4()
    response = await make_post_request(
        f"/films/watch/{film_id}/", headers=headers, settings=baseconfig
    )

    assert response.status == expected_status

    response_text = await response.text()
    response_data = json.loads(response_text)
    message = response_data.get("message")
    timestamp = response_data.get("timestamp")

    date_format = "%Y-%m-%d %H:%M:%S.%f"
    timestamp = datetime.datetime.strptime(timestamp, date_format).replace(second=0, microsecond=0)
    timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")

    assert message == expected_message
    assert timestamp == expected_timestamp


@pytest.mark.parametrize(
    "expected_status",
    [
        (HTTPStatus.FORBIDDEN),
    ],
)
async def test_post_film_timestamp_no_token(
    make_post_request: fixture,
    expected_status: int,
):
    headers = {"content-type": "application/json"}
    film_id = uuid.uuid4()
    response = await make_post_request(
        f"/films/watch/{film_id}/", headers=headers, settings=baseconfig
    )
    assert response.status == expected_status


@pytest.mark.parametrize(
    "expected_status, expected_message, expected_timestamp",
    [
        (HTTPStatus.OK, "OK", str(datetime.datetime.now().replace(second=0, microsecond=0))),
    ],
)
async def test_get_film_timestamp(
    get_jwt_token: fixture,
    make_post_request: fixture,
    make_get_request: fixture,
    expected_status: int,
    expected_message: str,
    expected_timestamp: str,
):
    token, _ = await get_jwt_token(settings=baseconfig)
    headers = {"Authorization": f"Bearer {token}", "content-type": "application/json"}
    film_id = uuid.uuid4()
    await make_post_request(f"/films/watch/{film_id}/", headers=headers, settings=baseconfig)
    response = await make_get_request(
        f"/films/watch/{film_id}/", headers=headers, settings=baseconfig
    )

    assert response.status == expected_status

    response_text = await response.text()
    response_data = json.loads(response_text)
    message = response_data.get("message")
    timestamp = response_data.get("timestamp")

    date_format = "%Y-%m-%d %H:%M:%S.%f"
    timestamp = datetime.datetime.strptime(timestamp, date_format).replace(second=0, microsecond=0)
    timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")

    assert message == expected_message
    assert timestamp == expected_timestamp


@pytest.mark.parametrize(
    "expected_status",
    [
        (HTTPStatus.FORBIDDEN),
    ],
)
async def test_get_film_timestamp_no_token(
    make_get_request: fixture,
    expected_status: int,
):
    headers = {"content-type": "application/json"}
    film_id = uuid.uuid4()
    response = await make_get_request(
        f"/films/watch/{film_id}/", headers=headers, settings=baseconfig
    )
    assert response.status == expected_status


@pytest.mark.parametrize(
    "expected_status",
    [
        (HTTPStatus.NOT_FOUND),
    ],
)
async def test_get_film_timestamp_not_found(
    get_jwt_token: fixture,
    make_get_request: fixture,
    expected_status: int,
):
    token, _ = await get_jwt_token(settings=baseconfig)
    headers = {"Authorization": f"Bearer {token}", "content-type": "application/json"}
    film_id = uuid.uuid4()
    response = await make_get_request(
        f"/films/watch/{film_id}/", headers=headers, settings=baseconfig
    )
    assert response.status == expected_status
