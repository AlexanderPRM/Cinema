from typing import List, Optional

from pydantic.main import BaseModel


class Context(BaseModel):
    users_id: Optional[List[str]]
    payload: dict
    link: Optional[str]


class Notification(BaseModel):
    template_id: Optional[str]
    notification_id: Optional[str]
    context: Context
