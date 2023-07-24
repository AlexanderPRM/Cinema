from http import HTTPStatus

import pytest
from pytest import fixture
from settings import baseconfig

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "expected_answer",
    [
        ({"status": HTTPStatus.OK},),
    ],
)
async def test_get_transactions_400(
    get_jwt_token: fixture,
    make_get_request: fixture,
    expected_answer: dict,
):
    token = await get_jwt_token(settings=baseconfig)
    headers = {"Authorization": f"Bearer {token[0]}", "content-type": "application/json"}
    cookies = {"access_token_cookie": token[0]}
    response = await make_get_request(
        baseconfig.PAYMENT_API_URL + "get_transactions/",
        headers=headers,
        settings=baseconfig,
        cookies=cookies,
    )
    assert response.status == expected_answer[0]["status"]


@pytest.mark.parametrize(
    "expected_answer",
    [
        ({"status": HTTPStatus.FORBIDDEN},),
    ],
)
async def test_transaction_handler_403(
    make_post_request: fixture,
    expected_answer: dict,
):
    response = await make_post_request(
        baseconfig.PAYMENT_API_URL + "transaction_handler/",
        settings=baseconfig,
    )
    assert response.status == expected_answer[0]["status"]
