import datetime
import json
import uuid
from http import HTTPStatus

import pytest
from pytest import fixture
from settings import baseconfig

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "expected_status, expected_message",
    [
        (HTTPStatus.CREATED, "Success"),
    ],
)
async def test_post_bookmark(
    get_jwt_token: fixture,
    make_post_request: fixture,
    expected_status: int,
    expected_message: str,
):
    token, _ = await get_jwt_token(settings=baseconfig)
    headers = {"Authorization": f"Bearer {token}", "content-type": "application/json"}
    film_id = uuid.uuid4()
    response = await make_post_request(
        f"films/bookmark/{film_id}/", headers=headers, settings=baseconfig
    )

    assert response.status == expected_status

    response_text = await response.text()
    response_data = json.loads(response_text)
    message = response_data.get("message")

    assert message == expected_message
