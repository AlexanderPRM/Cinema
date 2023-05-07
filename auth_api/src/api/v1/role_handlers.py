import json
from http import HTTPStatus

from flask import Blueprint, Response, abort, jsonify, make_response, request
from openapi_core import Spec, unmarshal_response
from openapi_core.contrib.flask.requests import FlaskOpenAPIRequest
from openapi_core.contrib.flask.responses import FlaskOpenAPIResponse

from core.permissions import superuser_required
from core.utils import is_uuid_valid
from db.models import User, UserRole
from db.postgres import db
from services.exception_service import HttpExceptions
from services.role_service import RoleService

role_bp = Blueprint("role", __name__, url_prefix="/role")
spec = Spec.from_file_path("openapi.yaml")


def name_validate(request):
    if "role_name" not in request.json:
        return abort(Response(json.dumps({"error_message": "Name not specified"}), 422))


@role_bp.route("/", methods=["GET"])
@superuser_required
def get_roles():
    roles = db.session.query(UserRole).all()
    roles = [{"id": role.id, "name": role.name} for role in roles]

    resp = jsonify({"roles": roles})
    # провеяем валидность ответа
    resp = make_response(resp, HTTPStatus.OK)
    unmarshal_response(FlaskOpenAPIRequest(request), FlaskOpenAPIResponse(resp), spec=spec)
    return resp


@role_bp.route("/", methods=["POST"])
@superuser_required
def create_role():
    name_validate(request)

    name = request.json["role_name"]
    if db.session.query(UserRole).filter_by(name=name).first():
        return HttpExceptions().already_exists("Role", name)

    role = UserRole(name=name)
    db.session.add(role)
    db.session.commit()

    resp = jsonify({"message": f"Role {name} created successfully"})
    return resp, HTTPStatus.CREATED


@role_bp.route("/<uuid:id>", methods=["DELETE"])
@superuser_required
def delete_role(id):
    role = db.session.query(UserRole).filter_by(id=id).first()
    if not role:
        resp = HttpExceptions().not_exists("Role", id)
        resp = make_response(resp, HTTPStatus.UNPROCESSABLE_ENTITY)
        unmarshal_response(FlaskOpenAPIRequest(request), FlaskOpenAPIResponse(resp), spec=spec)
        return resp

    db.session.delete(role)
    db.session.commit()

    resp = jsonify({"message": f"Role {role.id} deleted successfully"})
    return resp, HTTPStatus.OK


@role_bp.route("/<uuid:id>", methods=["PUT"])
@superuser_required
def update_role(id):
    name_validate(request)

    role = db.session.query(UserRole).filter_by(id=id).first()
    if not role:
        resp = HttpExceptions().not_exists("Role", id)
        resp = make_response(resp, HTTPStatus.UNPROCESSABLE_ENTITY)
        unmarshal_response(FlaskOpenAPIRequest(request), FlaskOpenAPIResponse(resp), spec=spec)
        return resp

    role.name = request.json["role_name"]
    db.session.commit()

    resp = jsonify({"message": f"Role {role.id} updated successfully"})
    return resp, HTTPStatus.OK


@role_bp.route("/change_role/<uuid:id>", methods=["PUT"])
@superuser_required
def change_role(id):
    role_name = request.json["role_name"]
    if not is_uuid_valid(id):
        return HttpExceptions().not_valid_uuid()
    role = RoleService().get(role_name)
    if not role:
        resp = HttpExceptions().not_exists("Role", role_name)
        resp = make_response(resp, HTTPStatus.UNPROCESSABLE_ENTITY)
        unmarshal_response(FlaskOpenAPIRequest(request), FlaskOpenAPIResponse(resp), spec=spec)
        return resp
    user = db.session.query(User).filter_by(id=id).first()
    if not user:
        resp = HttpExceptions().not_exists("User", id)
        resp = make_response(resp, HTTPStatus.UNPROCESSABLE_ENTITY)
        unmarshal_response(FlaskOpenAPIRequest(request), FlaskOpenAPIResponse(resp), spec=spec)
        return resp
    RoleService().change_user_role(role=role, user=user)
    resp = jsonify({"message": f"{user.email}'s role updated to {role.name} successfully"})
    return resp, HTTPStatus.OK


@role_bp.route("/change_role_to_default/<uuid:id>", methods=["PUT"])
@superuser_required
def change_role_to_default(id):
    if not is_uuid_valid(id):
        resp = HttpExceptions().not_valid_uuid()
        resp = make_response(resp, HTTPStatus.UNPROCESSABLE_ENTITY)
        unmarshal_response(FlaskOpenAPIRequest(request), FlaskOpenAPIResponse(resp), spec=spec)
        return resp
    user = db.session.query(User).filter_by(id=id).first()
    if not user:
        resp = HttpExceptions().not_exists("User", id)
        resp = make_response(resp, HTTPStatus.UNPROCESSABLE_ENTITY)
        unmarshal_response(FlaskOpenAPIRequest(request), FlaskOpenAPIResponse(resp), spec=spec)
        return resp
    RoleService().change_user_role_to_default(user=user)
    resp = jsonify({"message": f"{user.email}'s role updated to default successfully"})
    return resp, HTTPStatus.OK
