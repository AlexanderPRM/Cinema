import json
import uuid
from http import HTTPStatus

import pytest
from pytest import fixture
from settings import baseconfig

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"auto_renewal": True, "currency": "RUB", "idempotence_key": str(uuid.uuid4())},
            {"status": HTTPStatus.CREATED},
        ),
        (
            {
                "auto_renewal": True,
                "currency": "RUB",
            },
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
    ],
)
async def test_pay(
    get_jwt_token: fixture,
    make_post_request: fixture,
    query_data: dict,
    expected_answer: dict,
):
    token = await get_jwt_token(settings=baseconfig)
    headers = {"Authorization": f"Bearer {token[0]}", "content-type": "application/json"}
    cookies = {"access_token_cookie": token[0]}
    test_sub = {"title": "test_sub", "duration": 60, "cost": 999, "description": "some test sub"}
    response = await make_post_request(
        baseconfig.ADMIN_API_URL + "add/", headers=headers, query_data=test_sub, settings=baseconfig
    )
    response_text = await response.text()
    response_data = json.loads(response_text)
    sub_id = response_data["subscribe_id"]
    response = await make_post_request(
        baseconfig.BILLING_API_URL + f"pay/{sub_id}/",
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
            {"wrong_idempotence_key": str(uuid.uuid4()),},
            {"status": HTTPStatus.FORBIDDEN},
        ),
    ],
)
async def test_refund_403(
    get_jwt_token: fixture,
    make_post_request: fixture,
    query_data: dict,
    expected_answer: dict,
):
    token = await get_jwt_token(settings=baseconfig)
    headers = {"Authorization": f"Bearer {token[0]}", "content-type": "application/json"}
    cookies = {"access_token_cookie": token[0]}
    response = await make_post_request(
        baseconfig.BILLING_API_URL + "refund/",
        headers=headers,
        query_data=query_data["wrong_idempotence_key"],
        settings=baseconfig,
        cookies=cookies,
    )
    assert response.status == expected_answer["status"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"auto_renewal": True, "currency": "RUB", "idempotence_key": str(uuid.uuid4())},
            {"status": HTTPStatus.OK},
        ),
    ],
)
async def test_unsubscribe_200(
    get_jwt_token: fixture,
    make_post_request: fixture,
    make_get_request: fixture,
    query_data: dict,
    expected_answer: dict,
):
    token = await get_jwt_token(settings=baseconfig)
    headers = {"Authorization": f"Bearer {token[0]}", "content-type": "application/json"}
    cookies = {"access_token_cookie": token[0]}
    test_sub = {"title": "test_sub", "duration": 60, "cost": 999, "description": "some test sub"}
    response = await make_post_request(
        baseconfig.ADMIN_API_URL + "add/", headers=headers, query_data=test_sub, settings=baseconfig
    )
    response_text = await response.text()
    response_data = json.loads(response_text)
    sub_id = response_data["subscribe_id"]
    await make_post_request(
        baseconfig.BILLING_API_URL + f"pay/{sub_id}/",
        headers=headers,
        query_data=query_data,
        settings=baseconfig,
        cookies=cookies,
    )
    await make_get_request(
        baseconfig.PAYMENT_API_URL + "get_transactions/",
        headers=headers,
        settings=baseconfig,
        cookies=cookies,
    )
    response = await make_post_request(
        baseconfig.BILLING_API_URL + "unsubscribe/",
        headers=headers,
        settings=baseconfig,
        cookies=cookies,
    )
    assert response.status == expected_answer["status"]


@pytest.mark.parametrize(
    "expected_answer",
    [
        ({"status": HTTPStatus.FORBIDDEN},),
    ],
)
async def test_unsubscribe_403(
    get_jwt_token: fixture,
    make_post_request: fixture,
    expected_answer: dict,
):
    token = await get_jwt_token(settings=baseconfig)
    headers = {"Authorization": f"Bearer {token[0]}", "content-type": "application/json"}
    cookies = {"access_token_cookie": token[0]}
    response = await make_post_request(
        baseconfig.BILLING_API_URL + "unsubscribe/",
        headers=headers,
        settings=baseconfig,
        cookies=cookies,
    )
    assert response.status == expected_answer[0]["status"]
