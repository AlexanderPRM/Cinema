import asyncpg
from asyncpg.pool import Pool
from utils.config import pg_settings
from utils.logger import logger


class PostgresBase:
    def __init__(self):
        self.pool: Pool = None
        self.connection = None

    async def create_connection(self):
        self.pool = await asyncpg.create_pool(
            user=pg_settings.NOTF_POSTGRES_USER,
            password=pg_settings.NOTF_POSTGRES_PASSWORD,
            host=pg_settings.NOTF_POSTGRES_HOST,
            port=pg_settings.NOTF_POSTGRES_PORT,
            database=pg_settings.NOTF_POSTGRES_DB,
            min_size=5,
            max_size=10,
        )

    async def close_connection(self):
        await self.pool.close()

    async def select_query(self, query, params):
        async with self.pool.acquire() as connection:
            try:
                results = await connection.fetch(query, *params)
                return results
            except asyncpg.exceptions.PostgresError as e:
                logger.error(f"Error fetching query: {query}. Error message: {e}")
                raise

    async def set_query(self, query, params):
        async with self.pool.acquire() as connection:
            try:
                await connection.execute(query, *params)
            except asyncpg.exceptions.PostgresError as e:
                logger.error(f"Error executing query: {query}. Error message: {e}")
                raise
