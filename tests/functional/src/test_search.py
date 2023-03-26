import datetime
import logging
import uuid

import pytest
from pytest import fixture

#  Название теста должно начинаться со слова `test_`
#  Любой тест с асинхронными вызовами нужно оборачивать декоратором `pytest.mark.asyncio`,
#  который следит за запуском и работой цикла событий.


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"query": "The Star", "page_size": 50}, {
         "status": 200, "length": 50, "exists": True}),
        (
            {"query": "Mashed potato", "page_size": 50},
            {"status": 404, "length": 0, "exists": False},
        ),
    ],
)
@pytest.mark.asyncio
async def test_search(
    make_get_request: fixture, es_write_films_data: fixture, query_data: dict, expected_answer: dict
):
    # 1. Генерируем данные для ES

    es_data = [
        {
            "id": str(uuid.uuid4()),
            "imdb_rating": 8.5,
            "genre": ["Action", "Sci-Fi"],
            "title": "The Star",
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
        for _ in range(60)
    ]

    await es_write_films_data(es_data)

    # 3. Запрашиваем данные из ES по API

    response = await make_get_request("/api/v1/films/search", query_data)
    body = await response.json()
    status = response.status

    # 4. Проверяем ответ
    logging.info(body)
    assert status == expected_answer["status"]
    if expected_answer["exists"]:
        assert len(body) == expected_answer["length"]
    else:
        body.pop("detail")
        assert len(body) == expected_answer["length"]
