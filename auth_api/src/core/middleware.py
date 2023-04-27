import json
import time
from decimal import Decimal
from http import HTTPStatus

import redis
from flask import Response, abort

from core.config import config

MAX_TOKENS = config.MAX_TOKENS
SEC_FOR_TOKEN = config.SEC_FOR_TOKEN

redis_conn = redis.Redis(host=config.AUTH_REDIS_HOST, port=config.AUTH_REDIS_PORT, db=1)
redis_conn.set("tokens_amount", MAX_TOKENS)
redis_conn.set("last_refill_time", time.time())


def check_rate_limit():
    tokens_amount = int(redis_conn.get("tokens_amount"))
    last_refill_time = float(redis_conn.get("last_refill_time"))

    time_diff = time.time() - float(last_refill_time)
    tokens_to_add = int(time_diff / SEC_FOR_TOKEN)
    remainder = Decimal(f"{time_diff}") % Decimal(f"{SEC_FOR_TOKEN}")

    tokens_amount = min(tokens_amount + tokens_to_add, MAX_TOKENS)

    if tokens_to_add > 0:
        redis_conn.set("last_refill_time", time.time() - float(remainder))

    if tokens_amount > 0:
        redis_conn.set("tokens_amount", tokens_amount - 1)
    else:
        abort(
            Response(
                json.dumps({"message": "Too many requests, try later."}),
                HTTPStatus.TOO_MANY_REQUESTS,
            )
        )
