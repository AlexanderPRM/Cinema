import aiohttp
import backoff
import pytest_asyncio
import requests


@backoff.on_exception(
    backoff.expo,
    (
        requests.exceptions.ConnectionError,
        ConnectionRefusedError,
        aiohttp.client_exceptions.ClientConnectorError,
    ),
    max_tries=50,
    max_time=60,
)
@pytest_asyncio.fixture(scope="session", autouse=True)
async def aiohttp_client():
    client = aiohttp.ClientSession()
    yield client
    await client.close()
