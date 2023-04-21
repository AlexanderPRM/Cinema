from http import HTTPStatus

from flask import (
    Blueprint,
    Response,
    abort,
    json,
    jsonify,
    make_response,
    redirect,
    request,
    url_for,
)
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
    set_access_cookies,
    set_refresh_cookies,
    unset_access_cookies,
    unset_jwt_cookies,
    unset_refresh_cookies,
)
from jwt import decode as jwt_decode

from services.user_service import UserService
from core.config import config
from db.redis import redis_db

user_bp = Blueprint("user", __name__, url_prefix="/user")
jwt = JWTManager()
service = UserService()


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = redis_db.get(jti + "_access")
    return token_in_redis is not None


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
    redis_db.setex(
        str(user.id) + "_" + useragent + "_refresh",
        config.REFRESH_TOKEN_EXPIRES,
        refresh_token,
    )
    return resp, HTTPStatus.OK


@user_bp.route("/signup", methods=["POST"])
def signup():
    data_validate(request)
    email, password = request.json["email"], request.json["password"]
    name = request.json["name"] if "name" in request.json else None

    email, password, role, user = service.signup(email, password, name)
    access_token = create_access_token(identity=email, additional_claims={"role": role.name})
    refresh_token = create_refresh_token(identity=email)
    resp = jsonify(
        {"id": user.id, "tokens": {"access_token": access_token, "refresh_token": refresh_token}}
    )
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    user_agent = request.headers.get("User-Agent")
    redis_db.setex(
        str(user.id) + "_" + user_agent + "_refresh", config.REFRESH_TOKEN_EXPIRES, refresh_token
    )
    return resp, HTTPStatus.CREATED


@user_bp.route("/login_history", methods=["GET"])
@jwt_required(locations=["headers", "cookies"])
def login_history():
    service = UserService()
    user_email = get_jwt_identity()
    login_history = service.login_history(user_email)
    login_history_data = [
        {"user": h.user.email, "user_agent": h.user_agent, "auth_date": h.authentication_date}
        for h in login_history
    ]
    resp = jsonify({"login_history": login_history_data})
    return resp, HTTPStatus.OK


@user_bp.route("/refresh", methods=["POST"])  # POST
@jwt_required(locations=["headers", "cookies"], refresh=True)
def refresh():
    jti = get_jwt()["jti"]
    current_user = get_jwt_identity()
    user = service.get_profile_info(current_user)
    user_agent = request.headers.get("User-Agent")

    # проверка на наличие рефреш в бд
    refresh_token_cookie = request.cookies.get("refresh_token_cookie")
    refresh_from_storage = None
    redis_key = f"{user.id}_{user_agent}_refresh"
    refresh_from_storage = redis_db.get(redis_key)
    if refresh_from_storage is None:
        redis_key = f"{user.id}_admin-pc_refresh"
        refresh_from_storage = redis_db.get(redis_key)
    if refresh_from_storage is not None:
        refresh_from_storage = refresh_from_storage.decode("utf-8")
    if refresh_from_storage != refresh_token_cookie:
        return abort(
            Response(
                json.dumps({"error_message": "Not found or expired refresh_token"}),
                HTTPStatus.UNAUTHORIZED,
            )
        )

    access_token_cookie = request.cookies.get("access_token_cookie")
    jwt_data = decode_token(access_token_cookie, allow_expired=True)
    role = jwt_data.get("role")

    # Создаем новые токены
    access_token = create_access_token(identity=current_user, additional_claims={"role": role})
    refresh_token = create_refresh_token(identity=current_user)
    redis_db.setex(
        str(user.id) + "_" + user_agent + "_refresh", config.REFRESH_TOKEN_EXPIRES, refresh_token
    )

    resp = jsonify(
        {
            "old_refresh": refresh_token_cookie,
            "jti": jti,
            "tokens": {"access_token": access_token, "refresh_token": refresh_token},
        }
    )
    unset_refresh_cookies(resp)
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp, HTTPStatus.OK


@user_bp.route("/profile", methods=["GET"])  # GET
@jwt_required(locations=["headers", "cookies"])
def personal_info():
    access_token_cookie = request.cookies.get("access_token_cookie")
    jwt_data = jwt_decode(access_token_cookie, config.JWT_SECRET, algorithms=["HS256"])
    role = jwt_data["role"]
    current_user = get_jwt_identity()
    user_info = service.get_profile_info(current_user)
    resp = {"name": user_info.name, "email": current_user, "role": role}
    return resp, HTTPStatus.OK


@user_bp.route("/profile/name", methods=["POST"])  # POST
@jwt_required(locations=["headers", "cookies"])
def change_user_name():
    new_name = request.json["name"]
    current_user = get_jwt_identity()
    if new_name is not None:
        service.change_name(current_user, new_name)
        return jsonify({"Your NEW name: ": new_name}), HTTPStatus.OK
    name = service.get_profile_info(current_user).name
    return jsonify({"Your name: ": name}), HTTPStatus.OK


@user_bp.route("/profile/password", methods=["POST"])  # POST
@jwt_required(locations=["headers", "cookies"])
def change_user_password():
    new_password = request.json["new_password"]
    cur_password = request.json["password"]
    current_user = get_jwt_identity()
    if service.check_password(current_user, cur_password):
        service.change_password(current_user, new_password)
        return jsonify({"message": "You have successfully changed your password"}), HTTPStatus.OK
    return abort(Response(json.dumps({"error_message": "WRONG Password"}), HTTPStatus.FORBIDDEN))


@user_bp.route("/profile/email", methods=["POST"])  # POST
@jwt_required(locations=["headers", "cookies"])
def change_user_email():
    access_token_cookie = request.cookies.get("access_token_cookie")
    jwt_data = jwt_decode(access_token_cookie, config.JWT_SECRET, algorithms=["HS256"])
    role = jwt_data["role"]
    new_email = request.json["new_email"]
    password = request.json["password"]
    current_user = get_jwt_identity()
    if service.check_password(current_user, password):
        # создание токенов
        access_token = create_access_token(identity=new_email, additional_claims={"role": role})
        refresh_token = create_refresh_token(identity=new_email)
        # удаление access и refresh токенов
        resp = jsonify(
            {
                "NEW email: ": new_email,
                "NEWtokens": {"access_token": access_token, "refresh_token": refresh_token},
            }
        )
        unset_access_cookies(resp)
        unset_refresh_cookies(resp)
        # Изменение email
        service.change_email(email=current_user, new_email=new_email)
        # отправка токенов в куки
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
        return resp, HTTPStatus.OK
    return abort(Response(json.dumps({"error_message": "WRONG Password"}), HTTPStatus.FORBIDDEN))


@user_bp.route("/profile/logout", methods=["POST"])  # POST
@jwt_required(optional=True)
def logout():
    jti = get_jwt()["jti"]
    # Получаем id пользователя и юзер агент
    current_user = get_jwt_identity()
    user = service.get_profile_info(current_user)
    user_agent = request.headers.get("User-Agent")
    # Получаем токены
    access_token_cookie = request.cookies.get("access_token_cookie")
    # Записываем access токен, как устаревший
    redis_db.setex(jti + "_access", config.ACCESS_TOKEN_EXPIRES, access_token_cookie)
    # Удаляем из редис refresh
    redis_db.delete(str(user.id) + "_" + user_agent + "_refresh")
    resp = jsonify(
        {
            "id": user.id,
            "user-agent": user_agent,
            "jti": jti,
            "tokens": {"access_token": access_token_cookie},
        }
    )
    unset_jwt_cookies(resp)
    return resp, HTTPStatus.OK


@user_bp.route("/profile/delete", methods=["POST"])  # POST
@jwt_required(locations=["headers", "cookies"])
def delete():
    password = request.json["password"]
    current_user = get_jwt_identity()
    if not (service.check_password(current_user, password)):
        return abort(
            Response(json.dumps({"error_message": "WRONG Password"}), HTTPStatus.FORBIDDEN)
        )

    jti = get_jwt()["jti"]
    # Получаем id пользователя и юзер агент
    user = service.get_profile_info(current_user)
    user_agent = request.headers.get("User-Agent")
    # Получаем токены
    access_token_cookie = request.cookies.get("access_token_cookie")
    # Записываем access токен, как устаревший
    redis_db.setex(jti + "_access", config.ACCESS_TOKEN_EXPIRES, access_token_cookie)
    # Удаляем из редис refresh
    redis_db.delete(str(user.id) + "_" + user_agent + "_refresh")

    service.delete_account(current_user)

    resp = make_response(redirect(url_for("user.signup")))
    unset_jwt_cookies(resp)
    return resp, HTTPStatus.OK
