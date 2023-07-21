from models.base import OrjsonBaseModel


class Notification(OrjsonBaseModel):
    user_id: str | None
    ttl: int | None
    auto_renewal: bool | None
