import json
import uuid
from http import HTTPStatus

import jwt
import pytest
from pytest import fixture

from settings import baseconfig

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"role_name": "test_role"},
            {"status": HTTPStatus.CREATED, "roles": 1},
        ),
        (
            {"role_name": "test_role"},
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY, "roles": 1},
        ),
    ],
)
async def test_create_role(
    create_jwt_superuser_token: fixture,
    make_post_request_role: fixture,
    make_get_request_role: fixture,
    query_data: dict,
    expected_answer: dict,
):
    token = await create_jwt_superuser_token(settings=baseconfig)
    headers = {"Authorization": f"Bearer {token}", "content-type": "application/json"}
    response = await make_post_request_role(
        "/role/", headers=headers, query_data=query_data, settings=baseconfig
    )
    assert response.status == expected_answer["status"]
    response = await make_get_request_role("/role/", headers=headers, settings=baseconfig)
    response_text = await response.text()
    response_data = json.loads(response_text)
    assert len(response_data["roles"]) == expected_answer["roles"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"role_name": "test_role"},
            {"status": HTTPStatus.OK, "roles": 1},
        ),
    ],
)
async def test_get_role(
    create_jwt_superuser_token: fixture,
    make_post_request_role: fixture,
    make_get_request_role: fixture,
    query_data: dict,
    expected_answer: dict,
):
    token = await create_jwt_superuser_token(settings=baseconfig)
    headers = {"Authorization": f"Bearer {token}", "content-type": "application/json"}
    await make_post_request_role(
        "/role/", headers=headers, query_data=query_data, settings=baseconfig
    )
    response = await make_get_request_role("/role/", headers=headers, settings=baseconfig)
    response_text = await response.text()
    response_data = json.loads(response_text)
    assert response.status == expected_answer["status"]
    assert len(response_data["roles"]) == expected_answer["roles"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"role_name": "test_role_create"},
            {"status": HTTPStatus.OK},
        ),
    ],
)
async def test_delete_role_success(
    create_jwt_superuser_token: fixture,
    make_post_request_role: fixture,
    make_delete_request_role: fixture,
    make_get_request_role: fixture,
    query_data: dict,
    expected_answer: dict,
):
    token = await create_jwt_superuser_token(settings=baseconfig)
    headers = {"Authorization": f"Bearer {token}", "content-type": "application/json"}
    await make_post_request_role(
        "/role/", headers=headers, query_data=query_data, settings=baseconfig
    )
    response = await make_get_request_role("/role/", headers=headers, settings=baseconfig)
    response_text = await response.text()
    response_data = json.loads(response_text)
    role_id = response_data["roles"][0]["id"]
    response = await make_delete_request_role(
        f"/role/{role_id}", headers=headers, settings=baseconfig
    )
    assert response.status == expected_answer["status"]


@pytest.mark.parametrize(
    "expected_answer",
    [
        {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
    ],
)
async def test_delete_role_error(
    create_jwt_superuser_token: fixture,
    make_delete_request_role: fixture,
    expected_answer: dict,
):
    token = await create_jwt_superuser_token(settings=baseconfig)
    headers = {"Authorization": f"Bearer {token}", "content-type": "application/json"}
    role_id = uuid.uuid4()
    response = await make_delete_request_role(
        f"/role/{role_id}", headers=headers, settings=baseconfig
    )
    assert response.status == expected_answer["status"]


@pytest.mark.parametrize(
    "create_data, query_data, expected_answer",
    [
        (
            {"role_name": "test_role_create"},
            {"role_name": "change_me_role"},
            {"status": HTTPStatus.OK},
        ),
    ],
)
async def test_put_role_success(
    create_jwt_superuser_token: fixture,
    make_post_request_role: fixture,
    make_put_request_role: fixture,
    make_get_request_role: fixture,
    create_data: dict,
    query_data: dict,
    expected_answer: dict,
):
    token = await create_jwt_superuser_token(settings=baseconfig)
    headers = {"Authorization": f"Bearer {token}", "content-type": "application/json"}
    await make_post_request_role(
        "/role/", headers=headers, query_data=query_data, settings=baseconfig
    )
    response = await make_get_request_role("/role/", headers=headers, settings=baseconfig)
    response_text = await response.text()
    response_data = json.loads(response_text)
    role_id = response_data["roles"][0]["id"]
    response = await make_put_request_role(
        f"/role/{role_id}", query_data=create_data, headers=headers, settings=baseconfig
    )
    assert response.status == expected_answer["status"]
    response = await make_get_request_role("/role/", headers=headers, settings=baseconfig)
    response_text = await response.text()
    response_data = json.loads(response_text)
    assert response_data["roles"][0]["name"] == create_data["role_name"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"role_name": "change_me_role"},
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
    ],
)
async def test_put_role_error(
    create_jwt_superuser_token: fixture,
    make_put_request_role: fixture,
    query_data: dict,
    expected_answer: dict,
):
    token = await create_jwt_superuser_token(settings=baseconfig)
    headers = {"Authorization": f"Bearer {token}", "content-type": "application/json"}
    role_id = uuid.uuid4()
    response = await make_put_request_role(
        f"/role/{role_id}", query_data=query_data, headers=headers, settings=baseconfig
    )
    assert response.status == expected_answer["status"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"role_name": "test_role"},
            {"status": HTTPStatus.OK},
        ),
    ],
)
async def test_change_role_success(
    create_jwt_superuser_token: fixture,
    create_account: fixture,
    make_post_request_role: fixture,
    make_put_request_role: fixture,
    make_get_request_role: fixture,
    query_data: dict,
    expected_answer: dict,
):
    user_data = await create_account(settings=baseconfig)
    token = await create_jwt_superuser_token(settings=baseconfig)
    headers = {"Authorization": f"Bearer {token}", "content-type": "application/json"}
    await make_post_request_role(
        "/role/", headers=headers, query_data=query_data, settings=baseconfig
    )
    user_id = user_data.get("user_id")
    response = await make_put_request_role(
        f"/role/change_role/{user_id}",
        headers=headers,
        query_data=query_data,
        settings=baseconfig,
    )
    assert response.status == expected_answer["status"]
    response = await make_get_request_role("/role/", headers=headers, settings=baseconfig)
    response_text = await response.text()
    response_data = json.loads(response_text)
    roles = response_data.get("roles", [])
    changed_role = next((r for r in roles if r["name"] == query_data.get("role_name")), None)

    assert changed_role["name"] == query_data["role_name"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"role_name": "test_role_error"},
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
    ],
)
async def test_change_role_no_role_error(
    create_jwt_superuser_token: fixture,
    create_account: fixture,
    make_put_request_role: fixture,
    query_data: dict,
    expected_answer: dict,
):
    user_data = await create_account(settings=baseconfig)
    token = await create_jwt_superuser_token(settings=baseconfig)
    headers = {"Authorization": f"Bearer {token}", "content-type": "application/json"}
    user_id = user_data.get("user_id")
    response = await make_put_request_role(
        f"/role/change_role/{user_id}",
        headers=headers,
        query_data=query_data,
        settings=baseconfig,
    )
    assert response.status == expected_answer["status"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"role_name": "test_role"},
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
    ],
)
async def test_change_role_no_user_error(
    create_jwt_superuser_token: fixture,
    make_post_request_role: fixture,
    make_put_request_role: fixture,
    query_data: dict,
    expected_answer: dict,
):
    user_id = uuid.uuid4()
    token = await create_jwt_superuser_token(settings=baseconfig)
    headers = {"Authorization": f"Bearer {token}", "content-type": "application/json"}
    await make_post_request_role(
        "/role/", headers=headers, query_data=query_data, settings=baseconfig
    )
    response = await make_put_request_role(
        f"/role/change_role/{user_id}", headers=headers, query_data=query_data, settings=baseconfig
    )
    assert response.status == expected_answer["status"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"role_name": "supra_role"},
            {"status": HTTPStatus.OK, "role_name": "default"},
        ),
    ],
)
async def test_change_role_to_default_success(
    create_jwt_superuser_token: fixture,
    create_account: fixture,
    make_post_request_role: fixture,
    make_put_request_role: fixture,
    query_data: dict,
    expected_answer: dict,
):
    user_data = await create_account(settings=baseconfig)
    token = await create_jwt_superuser_token(settings=baseconfig)
    headers = {"Authorization": f"Bearer {token}", "content-type": "application/json"}
    await make_post_request_role(
        "/role/", headers=headers, query_data=query_data, settings=baseconfig
    )
    user_id = user_data.get("user_id")
    response = await make_put_request_role(
        f"/role/change_role/{user_id}",
        headers=headers,
        query_data=query_data,
        settings=baseconfig,
    )
    assert response.status == expected_answer["status"]
    user_id = user_data.get("user_id")
    response = await make_put_request_role(
        f"/role/change_role_to_default/{user_id}",
        headers=headers,
        settings=baseconfig,
    )
    payload = {
        "email": user_data.get("email"),
        "password": user_data.get("password"),
    }
    resp = await make_post_request_role("/user/signin", query_data=payload, settings=baseconfig)
    assert resp.status == expected_answer["status"]
    response_text = await resp.text()
    response_data = json.loads(response_text)
    token = response_data["tokens"]["access_token"]
    decoded_token = jwt.decode(token, baseconfig.jwt_secret, algorithms=["HS256"])
    role = decoded_token.get("role")
    assert role == expected_answer["role_name"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"role_name": "supra_role"},
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
    ],
)
async def test_change_role_to_default_error(
    create_jwt_superuser_token: fixture,
    create_account: fixture,
    make_post_request_role: fixture,
    make_put_request_role: fixture,
    query_data: dict,
    expected_answer: dict,
):
    user_data = await create_account(settings=baseconfig)
    token = await create_jwt_superuser_token(settings=baseconfig)
    headers = {"Authorization": f"Bearer {token}", "content-type": "application/json"}
    await make_post_request_role(
        "/role/", headers=headers, query_data=query_data, settings=baseconfig
    )
    user_id = user_data.get("user_id")
    response = await make_put_request_role(
        f"/role/change_role/{user_id}",
        headers=headers,
        query_data=query_data,
        settings=baseconfig,
    )
    new_user_id = uuid.uuid4()
    response = await make_put_request_role(
        f"/role/change_role_to_default/{new_user_id}", headers=headers, settings=baseconfig
    )
    assert response.status == expected_answer["status"]
