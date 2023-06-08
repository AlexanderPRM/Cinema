import asyncio
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
async def test_post_review(
    get_jwt_token: fixture,
    make_post_request: fixture,
    expected_status: int,
    expected_message: str,
):
    token, _ = await get_jwt_token(settings=baseconfig)
    headers = {"Authorization": f"Bearer {token}", "content-type": "application/json"}
    film_id = uuid.uuid4()
    query_data = {"text": "Test review"}
    response = await make_post_request(
        f"films/review/{film_id}/", headers=headers, settings=baseconfig, query_data=query_data
    )

    assert response.status == expected_status
    response_text = await response.text()
    response_data = json.loads(response_text)
    message = response_data.get("message")
    assert message == expected_message


@pytest.mark.parametrize(
    "get_status, post_status, expected_user_id, expected_film_id",
    [
        (HTTPStatus.OK, HTTPStatus.CREATED, str(uuid.uuid4()), str(uuid.uuid4())),
    ],
)
async def test_get_review(
    get_jwt_token: fixture,
    make_get_request: fixture,
    make_post_request: fixture,
    get_status: int,
    post_status: int,
    expected_user_id: str,
    expected_film_id: str,
):
    token, _ = await get_jwt_token(settings=baseconfig, user_uuid=expected_user_id)
    headers = {"Authorization": f"Bearer {token}", "content-type": "application/json"}
    film_id = expected_film_id
    query_data = {"text": "Test review"}
    response = await make_post_request(
        f"films/review/{film_id}/", headers=headers, settings=baseconfig, query_data=query_data
    )
    await asyncio.sleep(2)
    assert response.status == post_status
    params = {"sort_direction": "asc"}
    response = await make_get_request(
        f"films/review/{film_id}/", headers=headers, settings=baseconfig, params=params
    )
    assert response.status == get_status
    response_text = await response.text()
    response_data = json.loads(response_text)
    all_reviews = response_data.get("reviews")
    user_id = all_reviews[0].get("author")
    film_id = all_reviews[0].get("film_id")
    assert user_id == expected_user_id
    assert film_id == expected_film_id


@pytest.mark.parametrize(
    "get_status, post_status, expected_user_id, expected_film_id, expected_message",
    [
        (HTTPStatus.OK, HTTPStatus.CREATED, str(uuid.uuid4()), str(uuid.uuid4()), "Success"),
    ],
)
async def test_post_review_rate(
    get_jwt_token: fixture,
    make_get_request: fixture,
    make_post_request: fixture,
    get_status: int,
    post_status: int,
    expected_user_id: str,
    expected_film_id: str,
    expected_message: str,
):
    token, _ = await get_jwt_token(settings=baseconfig, user_uuid=expected_user_id)
    headers = {"Authorization": f"Bearer {token}", "content-type": "application/json"}
    film_id = expected_film_id
    query_data = {"text": "Test review"}
    response = await make_post_request(
        f"films/review/{film_id}/", headers=headers, settings=baseconfig, query_data=query_data
    )
    await asyncio.sleep(2)
    assert response.status == post_status
    params = {"sort_direction": "asc"}
    response = await make_get_request(
        f"films/review/{film_id}/", headers=headers, settings=baseconfig, params=params
    )
    assert response.status == get_status
    response_text = await response.text()
    response_data = json.loads(response_text)
    all_reviews = response_data.get("reviews")
    review_id = all_reviews[0].get("id")
    query_data = {"rate": 5}
    response = await make_post_request(
        f"films/review/rate/{review_id}/", headers=headers, settings=baseconfig, query_data=query_data
    )
    assert response.status == post_status
    response_text = await response.text()
    response_data = json.loads(response_text)
    message = response_data.get("message")
    assert message == expected_message


@pytest.mark.parametrize(
    "get_status, post_status, expected_user_id, expected_film_id, expected_message",
    [
        (HTTPStatus.OK, HTTPStatus.CREATED, str(uuid.uuid4()), str(uuid.uuid4()), "Success"),
    ],
)
async def test_put_review_rate(
    get_jwt_token: fixture,
    make_get_request: fixture,
    make_post_request: fixture,
    make_put_request: fixture,
    get_status: int,
    post_status: int,
    expected_user_id: str,
    expected_film_id: str,
    expected_message: str,
):
    token, _ = await get_jwt_token(settings=baseconfig, user_uuid=expected_user_id)
    headers = {"Authorization": f"Bearer {token}", "content-type": "application/json"}
    film_id = expected_film_id
    query_data = {"text": "Test review"}
    response = await make_post_request(
        f"films/review/{film_id}/", headers=headers, settings=baseconfig, query_data=query_data
    )
    await asyncio.sleep(2)
    assert response.status == post_status
    params = {"sort_direction": "asc"}
    response = await make_get_request(
        f"films/review/{film_id}/", headers=headers, settings=baseconfig, params=params
    )
    assert response.status == get_status
    response_text = await response.text()
    response_data = json.loads(response_text)
    all_reviews = response_data.get("reviews")
    review_id = all_reviews[0].get("id")
    query_data = {"rate": 5}
    response = await make_post_request(
        f"films/review/rate/{review_id}/", headers=headers, settings=baseconfig, query_data=query_data
    )
    assert response.status == post_status
    response_text = await response.text()
    response_data = json.loads(response_text)
    message = response_data.get("message")
    rate_id = response_data.get("_id")
    assert message == expected_message
    query_data = {"new_rate": 6}
    response = await make_put_request(
        f"films/review/rate/{rate_id}/", headers=headers, settings=baseconfig, query_data=query_data
    )
    assert response.status == post_status
    response_text = await response.text()
    response_data = json.loads(response_text)
    message = response_data.get("message")
    assert message == expected_message
