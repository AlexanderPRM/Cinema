from http import HTTPStatus

from core import config
from db.redis import redis_db
from flask import Blueprint, Response, abort, json, jsonify, request
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
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
    service = UserService()
    email = request.json.get("email")
    useragent = request.headers.get("User-Agent")
    password = request.json.get("password")
    email, role, user = service.signin(email=email, password=password, useragent=useragent)
    access_token = create_access_token(identity=email, additional_claims={"role": role.name})
    refresh_token = create_refresh_token(identity=email)
    resp = jsonify({"tokens": {"access_token": access_token, "refresh_token": refresh_token}})
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    redis_db.setex(str(user.id), config.config.REFRESH_TOKEN_EXPIRES, refresh_token)
    return resp, HTTPStatus.OK


@user_bp.route("/signup", methods=["POST"])
def signup():
    data_validate(request)
    email, password = request.json["email"], request.json["password"]
    name = request.json["name"] if "name" in request.json else None

    service = UserService()
    email, password, role, user = service.signup(email, password, name)
    access_token = create_access_token(identity=email, additional_claims={"role": role.name})
    refresh_token = create_refresh_token(identity=email)
    resp = jsonify(
        {"id": user.id, "tokens": {"access_token": access_token, "refresh_token": refresh_token}}
    )
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    redis_db.setex(str(user.id), config.config.REFRESH_TOKEN_EXPIRES, refresh_token)
    return resp, HTTPStatus.CREATED


@user_bp.route("/login_history", methods=["GET"])
@jwt_required()
def login_history():
    service = UserService()
    user_email = get_jwt_identity()
    login_history = service.login_history(user_email)
    login_history_data = [
        {"user": h.user.email, "user_agent": h.user_agent, "auth_date": h.authentication_date}
        for h in login_history
    ]
    resp = jsonify({"login_history": login_history_data})
    return resp, 200
