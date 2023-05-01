from abc import abstractmethod
from typing import Any

from core.config import config
from fastapi import HTTPException
from jose import jwt
from models.film import User


class BaseService:
    @abstractmethod
    async def get_by_id(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    async def get_by_param(self, *args, **kwargs) -> Any:
        pass


async def verify_jwt(request):
    token_cookie = request.cookies.get("access_token_cookie")

    if not token_cookie:
        raise HTTPException(status_code=401, detail="Token not found in cookies")
    try:
        payload = jwt.decode(token_cookie, config.JWT_SECRET, algorithms=["HS256"])
        return User(username=payload.get("sub"))
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
