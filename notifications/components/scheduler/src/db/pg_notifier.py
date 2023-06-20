from datetime import datetime
from enum import Enum
from functools import lru_cache

from db.pg_base import PostgresBase


class NotificationStatus(Enum):
    WAITING = "waiting"
    PROCESSING = "processing"
    DONE = "done"


class PostgresNotifier(PostgresBase):
    def __init__(self):
        super().__init__()

    async def create_connection(self):
        await super().create_connection()

    async def get_notification(self, task_type: str):
        sql_query = (
            "SELECT tasks.id task_id, tasks.template_id_id template_id, tasks.data task_data, tasks.task_type task_type, users_categories.category_name category_name "
            "FROM tasks "
            "LEFT JOIN users_categories ON users_categories.id = tasks.users_category_id "
            "WHERE tasks.pending_time <= $1 and tasks.send_status = $2 and task_type = $3"
        )
        params = (
            datetime.now(),
            NotificationStatus.WAITING.value,
            task_type,
        )
        result = await self.select_query(sql_query, params)
        return result

    async def set_status(self, task_id):
        sql_query = (
            "UPDATE tasks "
            "SET send_status = $1 "
            "WHERE id = $2"
        )
        params = (
            NotificationStatus.PROCESSING.value,
            task_id,
        )
        await self.set_query(sql_query, params)


@lru_cache()
def get_db_service() -> PostgresNotifier:
    return PostgresNotifier()
