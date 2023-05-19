from abc import abstractmethod
from typing import Any

from core.config import config
from fastapi import HTTPException
from jose import jwt
from redis.asyncio import Redis


class BaseService:
    @abstractmethod
    async def get_by_id(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    async def get_by_param(self, *args, **kwargs) -> Any:
        pass


async def verify_jwt(request):
    if not (config.JWT_REQUIER):
        return "No token required"
    token_cookie = request.cookies.get("access_token_cookie")
    redis_auth = Redis(host=config.AUTH_REDIS_HOST, port=config.AUTH_REDIS_PORT)

    if not token_cookie:
        raise HTTPException(status_code=401, detail="Token not found in cookies")
    try:
        payload = jwt.decode(token_cookie, config.JWT_SECRET, algorithms=["HS256"])
        jti = payload.get("jti")
        if await redis_auth.get(jti + "_access"):
            raise HTTPException(status_code=401, detail="Token can no longer be used")
        return payload.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
