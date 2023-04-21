from functools import wraps

from flask_jwt_extended.view_decorators import _decode_jwt_from_request, jwt_required


def superuser_required(fn):
    @wraps(fn)
    @jwt_required(locations=["headers", "cookies"])
    def wrapper(*args, **kwargs):
        data = _decode_jwt_from_request(locations=["headers", "cookies"], fresh=False)
        if data[0]["role"] != "superuser":
            return {"message": "Superuser only"}, 403
        return fn(*args, **kwargs)

    return wrapper
