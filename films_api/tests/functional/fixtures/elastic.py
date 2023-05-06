import json
import logging

import backoff
import elasticsearch
import pytest
import pytest_asyncio
import requests
from elasticsearch import AsyncElasticsearch

from settings import baseconfig


def get_es_bulk_query(es_data: list[dict], es_index: str, es_id_field: str) -> list:
    bulk_query = []
    for row in es_data:
        bulk_query.extend(
            [json.dumps({"index": {"_index": es_index, "_id": row[es_id_field]}}), json.dumps(row)]
        )
    return bulk_query


@pytest_asyncio.fixture(scope="session", autouse=True)
async def es_client():
    client = AsyncElasticsearch(hosts=baseconfig.es_adress, validate_cert=False, use_ssl=False)
    yield client
    await client.close()


@pytest.fixture
def es_write_data(es_client):
    @backoff.on_exception(
        backoff.expo,
        (
            requests.exceptions.ConnectionError,
            ConnectionRefusedError,
            elasticsearch.exceptions.ConnectionError,
        ),
        max_tries=50,
        max_time=60,
    )
    async def inner(data: list[dict], settings) -> None:
        bulk_query = get_es_bulk_query(data, settings.es_index, settings.es_id_field)
        str_query = "\n".join(bulk_query) + "\n"
        response = await es_client.bulk(str_query, refresh=True)
        logging.info(response)
        if response["errors"]:
            logging.error(response)
            raise Exception("Ошибка записи данных в Elasticsearch")

    return inner


@pytest.fixture
def es_clear_data(es_client):
    @backoff.on_exception(
        backoff.expo,
        (
            requests.exceptions.ConnectionError,
            ConnectionRefusedError,
            elasticsearch.exceptions.ConnectionError,
        ),
        max_tries=50,
        max_time=60,
    )
    async def inner(index):
        await es_client.delete_by_query(index=index, body={"query": {"match_all": {}}})

    return inner
