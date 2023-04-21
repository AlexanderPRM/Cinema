import json
import uuid
from http import HTTPStatus

import pytest
from pytest import fixture
from settings import baseconfig

pytestmark = pytest.mark.asyncio

email = str(uuid.uuid4().hex)[:10]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"email": f"{email}@mail.ru", "name": "Romel", "password": "1"},
            {"status": HTTPStatus.CREATED, "tokens": True},
        ),
        (
            {"email": "почтаmail|ru", "password": "1"},
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY, "tokens": False},
        ),
    ],
)
async def test_signup(
    make_post_request: fixture,
    query_data: dict,
    expected_answer: dict,
):
    """
    Test the sign-up functionality with valid user information.
    """
    resp = await make_post_request("/user/signup", query_data=query_data, settings=baseconfig)
    assert resp.status == expected_answer["status"]
    response_text = await resp.text()
    response_data = json.loads(response_text)
    assert ("tokens" in response_data.keys()) == expected_answer["tokens"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"email": f"{email}@mail.ru", "password": "1"}, {"status": HTTPStatus.OK, "tokens": True}),
        (
            {"email": "почтаmail|ru", "password": "1"},
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY, "tokens": False},
        ),
        (
            {"email": f"{email}@mail.ru", "password": "incorrect_passwd"},
            {"status": HTTPStatus.UNAUTHORIZED, "tokens": False},
        ),
    ],
)
async def test_signin(
    make_post_request: fixture,
    query_data: dict,
    expected_answer: dict,
):
    """
    Test the sign-in functionality with valid credentials.
    """
    resp = await make_post_request("/user/signin", query_data=query_data, settings=baseconfig)
    assert resp.status == expected_answer["status"]
    response_text = await resp.text()
    response_data = json.loads(response_text)
    assert ("tokens" in response_data.keys()) == expected_answer["tokens"]


email = str(uuid.uuid4().hex)[:10]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"cookies": True},
            {
                "status": HTTPStatus.OK,
                "email": f"{email}@mail.ru",
                "name": "Romel",
                "role": "default",
            },
        ),
        (
            {"cookies": False},
            {"status": HTTPStatus.UNAUTHORIZED, "email": None, "name": None, "role": None},
        ),
    ],
)
async def test_profile(
    get_access_token: fixture,
    make_get_request: fixture,
    query_data: dict,
    expected_answer: dict,
):
    """
    Test the user profile functionality which displays user information.
    """
    if query_data["cookies"]:
        # получаем access_token
        access_token = await get_access_token(settings=baseconfig, email=f"{email}@mail.ru")
    else:
        access_token = ""

    cookies = {"access_token_cookie": access_token}
    resp = await make_get_request("/user/profile", cookies=cookies, settings=baseconfig)
    assert resp.status == expected_answer["status"]
    response_text = await resp.text()
    response_data = json.loads(response_text)
    assert expected_answer["email"] == response_data.get("email")
    assert expected_answer["name"] == response_data.get("name")
    assert expected_answer["role"] == response_data.get("role")


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"name": "Deniska"}, {"status": HTTPStatus.OK}),
    ],
)
async def test_change_name(
    get_access_token: fixture,
    make_post_request: fixture,
    query_data: dict,
    expected_answer: dict,
):
    """
    Test the functionality to change the user name.
    """
    access_token = await get_access_token(settings=baseconfig)

    cookies = {"access_token_cookie": access_token}
    resp = await make_post_request(
        "/user/profile/name", cookies=cookies, query_data=query_data, settings=baseconfig
    )
    assert resp.status == expected_answer["status"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"new_password": "2", "password": "1"}, {"status": HTTPStatus.OK}),
        ({"new_password": "2", "password": "incorrect_passwd"}, {"status": HTTPStatus.FORBIDDEN}),
    ],
)
async def test_change_password(
    get_access_token: fixture,
    make_post_request: fixture,
    query_data: dict,
    expected_answer: dict,
):
    """
    Test the functionality to change the user password.
    """
    access_token = await get_access_token(settings=baseconfig)

    cookies = {"access_token_cookie": access_token}
    resp = await make_post_request(
        "/user/profile/password", cookies=cookies, query_data=query_data, settings=baseconfig
    )
    assert resp.status == expected_answer["status"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"new_email": str(uuid.uuid4().hex)[:10] + "@mail.ru", "password": "1"},
            {"status": HTTPStatus.OK},
        ),
        (
            {"new_email": str(uuid.uuid4().hex)[:10] + "@mail.ru", "password": "incorrect_passwd"},
            {"status": HTTPStatus.FORBIDDEN},
        ),
    ],
)
async def test_change_email(
    get_access_token: fixture,
    make_post_request: fixture,
    query_data: dict,
    expected_answer: dict,
):
    """
    Test the functionality to change the user email address.
    """
    access_token = await get_access_token(settings=baseconfig)

    cookies = {"access_token_cookie": access_token}
    resp = await make_post_request(
        "/user/profile/email", cookies=cookies, query_data=query_data, settings=baseconfig
    )
    assert resp.status == expected_answer["status"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({}, {"status": HTTPStatus.OK}),
    ],
)
async def test_logout(
    get_access_token: fixture,
    make_post_request: fixture,
    query_data: dict,
    expected_answer: dict,
):
    """
    Test the functionality to log out the user from the system.
    """
    access_token = await get_access_token(settings=baseconfig)

    cookies = {"access_token_cookie": access_token}
    resp = await make_post_request(
        "/user/profile/logout", cookies=cookies, query_data=query_data, settings=baseconfig
    )
    assert resp.status == expected_answer["status"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"password": "1"}, {"status": HTTPStatus.OK}),
        ({"password": "incorrect_passwd"}, {"status": HTTPStatus.FORBIDDEN}),
    ],
)
async def test_delete(
    get_access_token: fixture,
    make_post_request: fixture,
    query_data: dict,
    expected_answer: dict,
):
    """
    Test the functionality to delete the user account.
    """
    access_token = await get_access_token(settings=baseconfig)

    cookies = {"access_token_cookie": access_token}
    resp = await make_post_request(
        "/user/profile/delete", cookies=cookies, query_data=query_data, settings=baseconfig
    )
    assert resp.status == expected_answer["status"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({}, {"status": HTTPStatus.OK}),
    ],
)
async def test_login_history(
    get_access_token: fixture,
    make_get_request: fixture,
    make_post_request: fixture,
    query_data: dict,
    expected_answer: dict,
):
    """
    Test the functionality to view the user's login history.
    """
    email = f"{str(uuid.uuid4().hex)[:10]}@mail.ru"
    access_token = await get_access_token(settings=baseconfig, email=email)
    cookies = {"access_token_cookie": access_token}

    resp = await make_get_request("/user/login_history", cookies=cookies, settings=baseconfig)
    response_text = await resp.text()
    response_data = json.loads(response_text)
    assert response_data["login_history"] == []

    await make_post_request(
        "/user/signin", query_data={"email": email, "password": "1"}, settings=baseconfig
    )
    resp = await make_get_request("/user/login_history", cookies=cookies, settings=baseconfig)
    response_text = await resp.text()
    response_data = json.loads(response_text)
    assert len(response_data["login_history"]) == 1

@pytest.mark.parametrize(
    "expected_answer",
    [
        {"status": HTTPStatus.OK},
    ],
)
async def test_refresh_success(
    create_account: fixture,
    make_post_request_role: fixture,
    expected_answer: dict,
):
    user_data = await create_account(settings=baseconfig)
    user_refresh_token = user_data.get("tokens").get("refresh_token")
    resp = await make_post_request_role(
        "/user/refresh", query_data=user_refresh_token, settings=baseconfig
    )
    assert resp.status == expected_answer["status"]


@pytest.mark.parametrize(
    "expected_answer",
    [
        {"status": HTTPStatus.UNAUTHORIZED},
    ],
)
async def test_refresh_no_token_error(
    create_jwt_superuser_token: fixture,
    make_post_request_role: fixture,
    expected_answer: dict,
):
    token = await create_jwt_superuser_token(settings=baseconfig)
    resp = await make_post_request_role("/user/refresh", query_data=token, settings=baseconfig)
    assert resp.status == expected_answer["status"]
