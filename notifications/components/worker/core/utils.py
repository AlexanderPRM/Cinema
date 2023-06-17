from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt
from core.config import worker_setting


def generate_admin_jwt():
    now = datetime.now(timezone.utc)
    token_data = {
        "role": worker_setting.JWT_ADMIN_ROLE,
        "user_id": str(uuid4),
        "fresh": True,
        "jti": str(uuid4()),
        "nbf": now,
        "type": "access",
        "csrf": str(uuid4()),
        "exp": now + timedelta(seconds=604800),
        "sub": "admin",
    }
    return jwt.encode(token_data, key=worker_setting.JWT_SECRET)
