import json
import uuid
from http import HTTPStatus

import pytest
from pytest import fixture
from settings import baseconfig

pytestmark = pytest.mark.asyncio

sub = "test_sub_create" + str(uuid.uuid4().hex)[:10]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"title": sub, "duration": 150, "cost": 559, "description": "test subscribtion"},
            {"status": HTTPStatus.OK},
        ),
        (
            {"title": 123, "duration": 150, "cost": 559, "description": "test subscribtion"},
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
    ],
)
async def test_create_sub(
    get_jwt_token: fixture,
    make_post_request: fixture,
    query_data: dict,
    expected_answer: dict,
):
    token = await get_jwt_token(settings=baseconfig)
    headers = {"Authorization": f"Bearer {token[0]}", "content-type": "application/json"}
    cookies = {"access_token_cookie": token[0]}
    response = await make_post_request(
        baseconfig.ADMIN_API_URL + "add/",
        headers=headers,
        query_data=query_data,
        settings=baseconfig,
        cookies=cookies,
    )
    assert response.status == expected_answer["status"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {},
            {"status": HTTPStatus.OK},
        ),
    ],
)
async def test_get_transactions(
    get_jwt_token: fixture,
    make_get_request: fixture,
    query_data: dict,
    expected_answer: dict,
):
    token = await get_jwt_token(settings=baseconfig)
    headers = {"Authorization": f"Bearer {token[0]}", "content-type": "application/json"}
    cookies = {"access_token_cookie": token[0]}
    response = await make_get_request(
        baseconfig.ADMIN_API_URL + "transactions/",
        headers=headers,
        query_data=query_data,
        settings=baseconfig,
        cookies=cookies,
    )
    assert response.status == expected_answer["status"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"user_id": str(uuid.uuid4())},
            {"status": HTTPStatus.OK},
        ),
        (
            {"user_id": 123},
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
    ],
)
async def test_get_user_transactions(
    get_jwt_token: fixture,
    make_get_request: fixture,
    query_data: dict,
    expected_answer: dict,
):
    token = await get_jwt_token(settings=baseconfig)
    headers = {"Authorization": f"Bearer {token[0]}", "content-type": "application/json"}
    cookies = {"access_token_cookie": token[0]}
    response = await make_get_request(
        baseconfig.ADMIN_API_URL + f"transactions/{query_data['user_id']}/",
        headers=headers,
        settings=baseconfig,
        cookies=cookies,
    )
    assert response.status == expected_answer["status"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {
                "title": "test_sub",
                "duration": 60,
                "cost": 9999999,
                "description": "new description",
            },
            {"status": HTTPStatus.OK},
        ),
        (
            {"title": 123, "duration": 60, "cost": 9999999, "description": "new description"},
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
    ],
)
async def test_update_sub(
    get_jwt_token: fixture,
    make_put_request: fixture,
    make_post_request: fixture,
    query_data: dict,
    expected_answer: dict,
):
    token = await get_jwt_token(settings=baseconfig)
    headers = {"Authorization": f"Bearer {token[0]}", "content-type": "application/json"}
    cookies = {"access_token_cookie": token[0]}
    test_sub = {"title": "test_sub", "duration": 60, "cost": 999, "description": "some test sub"}
    response = await make_post_request(
        baseconfig.ADMIN_API_URL + "add/",
        headers=headers,
        query_data=test_sub,
        settings=baseconfig,
        cookies=cookies,
    )
    response_text = await response.text()
    response_data = json.loads(response_text)
    sub_id = response_data["subscribe_id"]
    response = await make_put_request(
        baseconfig.ADMIN_API_URL + f"update/{sub_id}/",
        headers=headers,
        query_data=query_data,
        settings=baseconfig,
        cookies=cookies,
    )
    assert response.status == expected_answer["status"]
