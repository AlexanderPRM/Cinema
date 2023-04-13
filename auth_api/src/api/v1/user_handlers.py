from core import config
from db.redis import redis_db
from flask import Blueprint, Response, abort, json, jsonify, request
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies,
)
from services.user_service import UserService

user_bp = Blueprint("user", __name__, url_prefix="/user")
jwt = JWTManager()


def data_validate(request):
    if "email" not in request.json or "password" not in request.json:
        return abort(
            Response(json.dumps({"error_message": "Email or Password not specified"}), 422)
        )


@user_bp.route("/signin", methods=["POST"])
def signin():
    data_validate(request)
    return "Success"


@user_bp.route("/signup", methods=["POST"])
def signup():
    data_validate(request)
    email, password = request.json["email"], request.json["password"]
    service = UserService()
    email, password, role, user = service.signup(email, password)
    access_token = create_access_token(identity=email, additional_claims={"role": role.name})
    refresh_token = create_refresh_token(identity=email)
    resp = jsonify(
        {"id": user.id, "tokens": {"access_token": access_token, "refresh_token": refresh_token}}
    )
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    redis_db.setex(str(user.id), config.config.REFRESH_TOKEN_EXPIRES, refresh_token)
    return resp, 201
