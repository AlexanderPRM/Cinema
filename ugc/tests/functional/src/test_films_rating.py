import datetime
import json
import uuid
from http import HTTPStatus

import pytest
from pytest import fixture
from settings import baseconfig

pytestmark = pytest.mark.asyncio

film_id = uuid.uuid4()


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        # Значения рейтинга не менять. Будет проверка подсчета среднего
        (
            {"film_id": film_id, "rating": 5},
            {"status": HTTPStatus.OK, "message": f"Successfully add rating 5 to film {film_id}"},
        ),
        (
            {"film_id": film_id, "rating": 123},
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY, "message": None},
        ),
        (
            {"film_id": film_id, "rating": 10},
            {"status": HTTPStatus.OK, "message": f"Successfully add rating 10 to film {film_id}"},
        ),
    ],
)
async def test_add_film_rating(
    get_jwt_token: fixture,
    make_post_request: fixture,
    query_data: dict,
    expected_answer: dict,
):
    token, _ = await get_jwt_token(settings=baseconfig)
    headers = {"Authorization": f"Bearer {token}", "content-type": "application/json"}
    response = await make_post_request(
        f"films/rating/{query_data['film_id']}/",
        query_data={"rating": query_data["rating"]},
        headers=headers,
        settings=baseconfig,
    )

    assert response.status == expected_answer["status"]

    response_text = await response.text()
    response_data = json.loads(response_text)
    message = response_data.get("message")
    assert message == expected_answer["message"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"film_id": film_id}, {"status": HTTPStatus.OK}),
        (
            {"film_id": str(film_id) + "not_valid_uuid_now"},
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
    ],
)
async def test_get_quantity_of_ratings(
    get_jwt_token: fixture,
    make_get_request: fixture,
    query_data: dict,
    expected_answer: dict,
):
    token, _ = await get_jwt_token(settings=baseconfig)
    headers = {"Authorization": f"Bearer {token}", "content-type": "application/json"}
    response = await make_get_request(
        f"films/rating/summary/{query_data['film_id']}/", headers=headers, settings=baseconfig
    )

    assert response.status == expected_answer["status"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"film_id": film_id}, {"status": HTTPStatus.OK, "Rating": 7.5}),
        (
            {"film_id": str(film_id) + "not_valid_uuid_now"},
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY, "Rating": None},
        ),
    ],
)
async def test_get_average_rating(
    get_jwt_token: fixture,
    make_get_request: fixture,
    query_data: dict,
    expected_answer: dict,
):
    token, _ = await get_jwt_token(settings=baseconfig)
    headers = {"Authorization": f"Bearer {token}", "content-type": "application/json"}
    response = await make_get_request(
        f"films/rating/{query_data['film_id']}/", headers=headers, settings=baseconfig
    )

    assert response.status == expected_answer["status"]

    response_text = await response.text()
    response_data = json.loads(response_text)
    message = response_data.get("Rating")
    assert message == expected_answer["Rating"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"film_id": str(film_id) + "not_valid_uuid_now"},
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY, "message": None},
        ),
        (
            {"film_id": film_id},
            {"status": HTTPStatus.BAD_REQUEST, "message": "The user has not yet rated this movie"},
        ),
    ],
)
async def test_delete_rating(
    get_jwt_token: fixture,
    make_delete_request: fixture,
    make_post_request: fixture,
    query_data: dict,
    expected_answer: dict,
):
    token, _ = await get_jwt_token(settings=baseconfig)
    headers = {"Authorization": f"Bearer {token}", "content-type": "application/json"}

    response = await make_delete_request(
        f"films/rating/delete/{query_data['film_id']}/", headers=headers, settings=baseconfig
    )

    assert response.status == expected_answer["status"]

    response_text = await response.text()
    response_data = json.loads(response_text)
    message = response_data.get("message")
    assert message == expected_answer["message"]
