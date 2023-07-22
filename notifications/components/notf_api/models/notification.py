from enum import Enum
from typing import List, Optional

from pydantic.main import BaseModel


class TypeEnum(str, Enum):
    new_episodes = "new_episodes"
    email_confirm = "email_confirm"
    recommendations = "recommendations"
    person_likes = "person_likes"
    subscribe_info = "subscribe_info"


class Context(BaseModel):
    users_id: Optional[List[str]]
    payload: dict
    link: Optional[str]


class Notification(BaseModel):
    type_send: TypeEnum = TypeEnum.new_episodes
    template_id: Optional[str]
    notification_id: Optional[str]
    context: Context
