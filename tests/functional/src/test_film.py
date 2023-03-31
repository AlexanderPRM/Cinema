import datetime
import logging
import uuid

import pytest
from pytest import fixture

from ..settings import films_settings


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"page_size": 5}, {"status": 200, "length": 5}),
        ({"page_size": 50, "page_number": 50}, {"status": 404, "length": 1}),
    ],
)
@pytest.mark.asyncio
async def test_film(
    make_get_request: fixture,
    es_write_data: fixture,
    es_clear_data: fixture,
    query_data: dict,
    expected_answer: dict,
):
    # Очищаем данные из ElsticSearch
    await es_clear_data(films_settings.es_index)
    # Записываем данные в ElsticSearch
    es_data = [
        {
            "id": str(uuid.uuid4()),
            "imdb_rating": 8.5,
            "genre": [
                {"id": "111", "name": "Action"},
                {"id": "222", "name": "Sci-Fi"}
            ],
            "title": "Aboba Bumba",
            "description": "New World",
            "director": ["Stan"],
            "actors_names": ["Ann", "Bob"],
            "writers_names": ["Ben", "Howard"],
            "actors": [{"id": "111", "name": "Ann"}, {"id": "222", "name": "Bob"}],
            "writers": [{"id": "333", "name": "Ben"}, {"id": "444", "name": "Howard"}],
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat(),
            "film_work_type": "movie",
        }
        for _ in range(5)
    ]
    await es_write_data(es_data, settings=films_settings)

    # Делаем запрос к API с предписанными параметрами
    resp = await make_get_request("/api/v1/films/", query_data=query_data, settings=films_settings)
    body = await resp.json()
    status = resp.status

    logging.error(body)
    # Проверяем response на expected_answer
    assert status == expected_answer["status"]
    assert len(body) == expected_answer["length"]


@pytest.mark.parametrize(
    "id_query_data, id_expected_answer",
    [
        (
            {"ID": "40ebbe7c-9ed8-4986-a4ff-6a5918890178"},
            {"status": 200, "id": "40ebbe7c-9ed8-4986-a4ff-6a5918890178"},
        ),
        ({"ID": "40ebbe7c-9ed8-4986-a4ff-6a5555555555"}, {"status": 404, "id": None}),
    ],
)
@pytest.mark.asyncio
async def test_id_film(
    make_get_request: fixture,
    es_write_data: fixture,
    es_clear_data: fixture,
    id_query_data: dict,
    id_expected_answer: dict,
):
    es_data = [
        {
            "id": "40ebbe7c-9ed8-4986-a4ff-6a5918890178",
            "imdb_rating": 8.5,
            "genre": [
                {"id": "111", "name": "Action"},
                {"id": "222", "name": "Sci-Fi"}
                ],
            "title": "Aboba Bumba",
            "description": "New World",
            "director": ["Stan"],
            "actors_names": ["Ann", "Bob"],
            "writers_names": ["Ben", "Howard"],
            "actors": [{"id": "111", "name": "Ann"}, {"id": "222", "name": "Bob"}],
            "writers": [{"id": "333", "name": "Ben"}, {"id": "444", "name": "Howard"}],
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat(),
            "film_work_type": "movie",
        }
    ]
    await es_write_data(es_data, settings=films_settings)

    resp = await make_get_request("/api/v1/films/%s" % id_query_data["ID"], settings=films_settings)
    if resp is not None:
        body = await resp.json()
        status = resp.status

        logging.error(body)
        # Проверяем response на expected_answer
        assert status == id_expected_answer["status"]
        if "detail" not in body.keys():
            assert body["id"] == id_expected_answer["id"]
