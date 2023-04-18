from functools import wraps

from flask_jwt_extended import current_user


def superuser_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if current_user.role.name != "superuser":
            return {"message": "Superuser only"}, 403
        return fn(*args, **kwargs)

    return wrapper
