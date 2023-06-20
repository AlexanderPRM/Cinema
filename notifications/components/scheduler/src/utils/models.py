from typing import List, Optional

from pydantic.main import BaseModel


class Context(BaseModel):
    users_id: Optional[List[str]]
    payload: Optional[dict]
    link: Optional[str]


class Notification(BaseModel):
    template_id: Optional[str]
    type_send: str
    notification_id: str
    context: Context
    category_name: Optional[str]
