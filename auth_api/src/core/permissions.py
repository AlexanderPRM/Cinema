from functools import wraps

from flask_jwt_extended import current_user


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if current_user.role.name != "admin":
            return {"message": "Admins only"}, 403
        return fn(*args, **kwargs)

    return wrapper
