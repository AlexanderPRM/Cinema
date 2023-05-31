import logging
from typing import Optional

import jwt
from core.config import config
from fastapi import Cookie, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request, access_token_cookie: Optional[str] = Cookie(None)):
        token = access_token_cookie if access_token_cookie else None
        if not token:
            credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(
                request
            )
            token = credentials.credentials
        try:
            return jwt.decode(token, config.JWT_SECRET, algorithms=["HS256"])
        except (jwt.exceptions.ExpiredSignatureError, jwt.exceptions.DecodeError) as err:
            logging.error(err)
            return
