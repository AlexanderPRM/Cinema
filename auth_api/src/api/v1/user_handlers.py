from flask import Blueprint, abort, request

user_bp = Blueprint("user", __name__, url_prefix="/user")


def data_validate(request):
    if "email" not in request.json or "password" not in request.json:
        abort(400)


@user_bp.route("/signin", methods=["POST"])
def signin():
    data_validate(request)
    return "Success"


@user_bp.route("/signun", methods=["POST"])
def signup():
    pass


# И тд
