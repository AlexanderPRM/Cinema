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


@pytest.mark.parametrize(
    "get_status, post_status, expected_message, expected_user_id, expected_film_id",
    [
        (HTTPStatus.OK, HTTPStatus.CREATED, "Success", str(uuid.uuid4()), str(uuid.uuid4())),
    ],
)
async def test_get_bookmark(
    get_jwt_token: fixture,
    make_get_request: fixture,
    make_post_request: fixture,
    get_status: int,
    post_status: int,
    expected_message: str,
    expected_user_id: str,
    expected_film_id: str,
):
    token, _ = await get_jwt_token(settings=baseconfig, user_uuid=expected_user_id)
    headers = {"Authorization": f"Bearer {token}", "content-type": "application/json"}
    film_id = expected_film_id
    response = await make_post_request(
        f"films/bookmark/{film_id}/", headers=headers, settings=baseconfig
    )
    assert response.status == post_status
    response = await make_get_request("films/bookmark/", headers=headers, settings=baseconfig)
    assert response.status == get_status
    response_text = await response.text()
    response_data = json.loads(response_text)
    message = response_data.get("message")
    user_id = response_data.get("user_id")
    film_id = response_data.get("data")[0].get("film_id")
    assert message == expected_message
    assert user_id == expected_user_id
    assert film_id == expected_film_id


@pytest.mark.parametrize(
    "post_status, delete_status, expected_message",
    [
        (HTTPStatus.CREATED, HTTPStatus.OK, "Success"),
    ],
)
async def test_delete_bookmark_success(
    get_jwt_token: fixture,
    make_post_request: fixture,
    make_delete_request: fixture,
    post_status: int,
    delete_status: int,
    expected_message: str,
):
    token, _ = await get_jwt_token(settings=baseconfig)
    headers = {"Authorization": f"Bearer {token}", "content-type": "application/json"}
    film_id = uuid.uuid4()
    response = await make_post_request(
        f"films/bookmark/{film_id}/", headers=headers, settings=baseconfig
    )
    assert response.status == post_status
    response = await make_delete_request(
        f"films/bookmark/{film_id}/", headers=headers, settings=baseconfig
    )
    assert response.status == delete_status
    response_text = await response.text()
    response_data = json.loads(response_text)
    message = response_data.get("message")
    assert message == expected_message


@pytest.mark.parametrize(
    "delete_status, expected_message",
    [
        (HTTPStatus.NOT_FOUND, "Bookmark doesnt exist"),
    ],
)
async def test_delete_bookmark_not_found(
    get_jwt_token: fixture,
    make_delete_request: fixture,
    delete_status: int,
    expected_message: str,
):
    token, _ = await get_jwt_token(settings=baseconfig)
    headers = {"Authorization": f"Bearer {token}", "content-type": "application/json"}
    film_id = uuid.uuid4()
    response = await make_delete_request(
        f"films/bookmark/{film_id}/", headers=headers, settings=baseconfig
    )
    assert response.status == delete_status
    response_text = await response.text()
    response_data = json.loads(response_text)
    message = response_data.get("detail")
    assert message == expected_message
