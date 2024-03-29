import logging
import uuid
from http import HTTPStatus

import pytest
from pytest import fixture

from ..settings import genre_setting

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"query": "2281e359-4080-421f-a015-517d31ca8044"}, {"status": HTTPStatus.OK}),
        ({"query": "00000000-0000-0000-0000-000000000000"}, {"status": HTTPStatus.NOT_FOUND}),
        ({"query": "000"}, {"status": HTTPStatus.UNPROCESSABLE_ENTITY}),
    ],
)
async def test_genres_by_id(
    make_get_request_id: fixture,
    es_write_data: fixture,
    query_data: dict,
    expected_answer: dict,
):
    es_data = [{"id": "2281e359-4080-421f-a015-517d31ca8044", "name": "created_genre"}]

    await es_write_data(es_data, genre_setting)

    response = await make_get_request_id(
        "/api/v1/genres/", query_data=query_data["query"], settings=genre_setting
    )
    body = await response.json()
    status = response.status

    logging.info(body)
    assert status == expected_answer["status"].value


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"page_size": 10}, {"status": HTTPStatus.OK, "length": 10}),
        ({"page_size": 10, "page_number": 500}, {"status": HTTPStatus.NOT_FOUND, "length": 1}),
        (
            {"page_size": "page_size", "page_number": "page_number"},
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY, "length": 1},
        ),
    ],
)
async def test_genres_list(
    make_get_request: fixture,
    es_write_data: fixture,
    query_data: dict,
    expected_answer: dict,
):
    es_data = [
        {
            "id": str(uuid.uuid4()),
            "name": "test_genre",
        }
        for _ in range(60)
    ]

    await es_write_data(es_data, genre_setting)

    response = await make_get_request(
        "/api/v1/genres/", query_data=query_data, settings=genre_setting
    )
    body = await response.json()
    status = response.status

    logging.info(body)
    assert status == expected_answer["status"].value
    assert len(body) == expected_answer["length"]
