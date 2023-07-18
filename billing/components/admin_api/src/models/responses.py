from typing import List

from pydantic import BaseModel


class AddSubscribtion(BaseModel):
    message: str
    subscribe_id: str | None


class UpdateSub(BaseModel):
    message: str
    users_autorenewal_disabled: List[str]
