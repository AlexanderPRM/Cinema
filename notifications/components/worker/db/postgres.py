import asyncpg
from core.config import postgres_settings


class PostgreSQLConsumer:
    def __init__(self, connection) -> None:
        self.connection: asyncpg.connection = connection

    async def get_template(self, template_id):
        return await self.connection.fetch(
            "SELECT * FROM %s WHERE id = '%s'" % (postgres_settings.TEMPLATE_TABLE, template_id)
        )
