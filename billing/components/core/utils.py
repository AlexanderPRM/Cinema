from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt
from core.config import config
from fastapi import Query


def generate_admin_jwt():
    now = datetime.now(timezone.utc)
    token_data = {
        "role": config.JWT_ADMIN_ROLE,
        "user_id": str(uuid4()),
        "fresh": True,
        "jti": str(uuid4()),
        "nbf": now,
        "type": "access",
        "csrf": str(uuid4()),
        "exp": now + timedelta(seconds=604800),
        "sub": "admin",
    }
    return jwt.encode(token_data, key=config.JWT_SECRET)


class CommonQueryParams:
    def __init__(
        self,
        page_number: int | None = Query(default=1, ge=1),
        page_size: int | None = Query(default=10, ge=1, le=50),
    ):
        self.page_number = page_number
        self.page_size = page_size
