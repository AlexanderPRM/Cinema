import logging
import uuid

import pytest
from pytest import fixture


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"query": "2281e359-4080-421f-a015-517d31ca8041"},
            {"status": 200}
        ),
        (
            {"query": "00000000-0000-0000-0000-000000000000"},
            {"status": 404}
        ),
    ],
)
@pytest.mark.asyncio
async def test_persons_by_id(
    make_get_request_persons: fixture, es_write_persons_data: fixture, query_data: dict, expected_answer: dict
):
    es_data = [{
        "id": "2281e359-4080-421f-a015-517d31ca8041",
        "full_name": "created_person",
        "films": [{}]
    }]

    await es_write_persons_data(es_data)

    response = await make_get_request_persons("/api/v1/persons/", query_data["query"])
    body = await response.json()
    status = response.status

    logging.info(body)
    assert status == expected_answer["status"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"page_size": 10},
            {"status": 200, "length": 10}
        ),
        (
            {"page_size": 10, "page_number": 500},
            {"status": 404, "length": 1}
        ),
    ],
)
@pytest.mark.asyncio
async def test_persons_list(
    make_get_request: fixture, es_write_persons_data: fixture, query_data: dict, expected_answer: dict
):
    es_data = [
        {
            "id": str(uuid.uuid4()),
            "full_name": "test_person",
        }
        for _ in range(60)
    ]

    await es_write_persons_data(es_data)

    response = await make_get_request("/api/v1/persons/", query_data)
    body = await response.json()
    status = response.status

    logging.info(body)
    assert status == expected_answer["status"]
    assert len(body) == expected_answer["length"]
