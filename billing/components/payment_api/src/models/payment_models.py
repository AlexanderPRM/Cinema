from models.base import OrjsonBaseModel


class Payment_info(OrjsonBaseModel):
    payment_id: str


class Notification(OrjsonBaseModel):
    user_id: str | None
    ttl: int | None
    auto_renewal: bool | None
