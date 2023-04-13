from core.config import config
from flask import (Blueprint,
                   Response,
                   abort,
                   json,
                   jsonify,
                   make_response,
                   redirect,
                   render_template,
                   request,
                   url_for,)
from flask_jwt_extended import (JWTManager,
                                create_access_token,
                                create_refresh_token,
                                decode_token,
                                get_jwt_identity,
                                jwt_required,
                                set_access_cookies,
                                set_refresh_cookies,
                                unset_access_cookies,
                                unset_jwt_cookies,
                                unset_refresh_cookies,
                                verify_jwt_in_request,)
from jwt import InvalidTokenError
from jwt import decode as jwt_decode
from services.user_service import UserService

user_bp = Blueprint("user", __name__, url_prefix="/user")
jwt = JWTManager()


def data_validate(request):
    if "email" not in request.json or "password" not in request.json:
        return abort(
            Response(json.dumps({"error_message": "Email or Password not specified"}), 422)
        )


@user_bp.route("/signup", methods=["POST"])
def signup():
    data_validate(request)
    email, password, name = request.json["email"], request.json["password"], request.json["name"]
    service = UserService()
    email, password, role, user = service.signup(email, password, name)
    access_token = create_access_token(identity=email, additional_claims={"role": role.name})
    refresh_token = create_refresh_token(identity=email)
    resp = jsonify(
        {"id": user.id, "tokens": {"access_token": access_token, "refresh_token": refresh_token}}
    )
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp, 201


@user_bp.route("/refresh", methods=["GET", "POST"])  # POST
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()

    access_token_cookie = request.cookies.get("access_token_cookie")
    jwt_data = decode_token(access_token_cookie, allow_expired=True)
    role = jwt_data.get("role")

    access_token = create_access_token(identity=current_user, additional_claims={"role": role})
    refresh_token = create_refresh_token(identity=current_user)

    service = UserService()
    id = service.refresh(current_user)

    resp = jsonify(
        {
            "id": id,
            "role": role,
            "user": str(id),
            "tokens": {"access_token": access_token, "refresh_token": refresh_token},
        }
    )
    unset_refresh_cookies(resp)
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp


@user_bp.route("/profile", methods=["GET", "POST"])  # GET
@jwt_required()
def personal_info():
    access_token_cookie = request.cookies.get("access_token_cookie")
    jwt_data = jwt_decode(access_token_cookie, config.JWT_SECRET, algorithms=["HS256"])
    role = jwt_data["role"]

    current_user = get_jwt_identity()

    service = UserService()
    user_info = service.get_profile_info(current_user)

    user_data = {"name": user_info.name, "email": current_user, "role": role}
    return render_template("profile.html", current_user=current_user, **user_data)


@user_bp.route("/profile/name", methods=["GET", "POST"])  # POST
@jwt_required()
def change_user_name():
    service = UserService()
    new_name = request.json["name"]
    current_user = get_jwt_identity()
    if new_name is not None:
        service.change_name(current_user, new_name)
        return jsonify({"Your NEW name: ": new_name})
    else:
        name = service.get_profile_info(current_user).name
        return jsonify({"Your name: ": name})


@user_bp.route("/profile/password", methods=["GET", "POST"])  # POST
@jwt_required()
def change_user_password():
    service = UserService()
    new_password = request.json["new_password"]
    cur_password = request.json["password"]
    current_user = get_jwt_identity()
    if service.check_password(current_user, cur_password):
        service.change_password(current_user, new_password)
        return jsonify({"Your NEW password: ": new_password})
    else:
        return abort(Response(json.dumps({"error_message": "WRONG Password"}), 403))


@user_bp.route("/profile/email", methods=["GET", "POST"])  # POST
@jwt_required()
def change_user_email():
    access_token_cookie = request.cookies.get("access_token_cookie")
    jwt_data = jwt_decode(access_token_cookie, config.JWT_SECRET, algorithms=["HS256"])
    role = jwt_data["role"]
    service = UserService()
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
        return resp
    else:
        return abort(Response(json.dumps({"error_message": "WRONG Password"}), 403))


@user_bp.route("/profile/logout")  # POST
@jwt_required()
def logout():
    resp = make_response(redirect(url_for("user.signup")))
    unset_jwt_cookies(resp)
    return resp
