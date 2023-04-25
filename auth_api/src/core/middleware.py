import json
import time
from decimal import Decimal
from http import HTTPStatus

import redis
from flask import Response, abort

from core.config import config

MAX_TOKENS = 100000
SEC_FOR_TOKEN = 0.001

redis_conn = redis.Redis(host=config.AUTH_REDIS_HOST, port=config.AUTH_REDIS_PORT, db=1)
redis_conn.set('tokens', MAX_TOKENS)
redis_conn.set('last_refill_time', time.time())

def check_rate_limit():
    tokens = int(redis_conn.get('tokens'))
    last_refill_time = float(redis_conn.get('last_refill_time'))

    elapsed_time = time.time() - float(last_refill_time)
    tokens_to_add = int(elapsed_time / SEC_FOR_TOKEN)
    remainder = Decimal(f"{elapsed_time}") % Decimal(f"{SEC_FOR_TOKEN}")

    tokens = min(tokens + tokens_to_add, MAX_TOKENS)

    if tokens_to_add > 0:
        redis_conn.set('last_refill_time', time.time() - float(remainder))

    if tokens > 0:
        redis_conn.set('tokens', tokens - 1)
    else:
        abort(
            Response(
                json.dumps({"message": "Too many requests, try later."}),
                HTTPStatus.TOO_MANY_REQUESTS,
            )
        )
