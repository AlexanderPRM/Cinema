import logging
import uuid

import pytest
from pytest import fixture

from ..settings import genre_setting


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"query": "2281e359-4080-421f-a015-517d31ca8044"}, {"status": 200}),
        ({"query": "00000000-0000-0000-0000-000000000000"}, {"status": 404}),
    ],
)
@pytest.mark.asyncio
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
    assert status == expected_answer["status"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"page_size": 10}, {"status": 200, "length": 10}),
        ({"page_size": 10, "page_number": 500}, {"status": 404, "length": 1}),
    ],
)
@pytest.mark.asyncio
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
    assert status == expected_answer["status"]
    assert len(body) == expected_answer["length"]
