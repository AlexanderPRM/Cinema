from db.models import UserRole
from db.postgres import db
from flask import Blueprint, Response, abort, json, jsonify, request
from flask_jwt_extended.view_decorators import _decode_jwt_from_request, jwt_required
from services.exception_service import HttpExceptions

role_bp = Blueprint("role", __name__, url_prefix="/role")


def name_validate(request):
    if "role_name" not in request.json:
        return abort(Response(json.dumps({"error_message": "Name not specified"}), 422))


def permission_validate(data: dict):
    if "superuser" != data["role"]:
        return abort(Response(json.dumps({"error_message": "Permission Denied"}), 403))


@jwt_required(True, locations=["headers", "cookies"])
@role_bp.route("/", methods=["GET"])
def get_roles():
    data = _decode_jwt_from_request(locations=["headers", "cookies"], fresh=False)
    permission_validate(data[0], "superuser")

    roles = db.session.query(UserRole).all()
    roles = [{"id": role.id, "name": role.name} for role in roles]

    resp = jsonify({"roles": roles})
    return resp, 200


@jwt_required(True, locations=["headers", "cookies"])
@role_bp.route("/", methods=["POST"])
def create_role():
    data = _decode_jwt_from_request(locations=["headers", "cookies"], fresh=False)
    permission_validate(data[0])
    name_validate(request)

    name = request.json["role_name"]
    if db.session.query(UserRole).filter_by(name=name).first():
        return HttpExceptions().already_exists("Role", name)

    role = UserRole(name=name)
    db.session.add(role)
    db.session.commit()

    resp = jsonify({"message": f"Role {name} created success"})
    return resp, 201


@jwt_required(True, locations=["headers", "cookies"])
@role_bp.route("/<uuid:id>", methods=["DELETE"])
def delete_role(id):
    data = _decode_jwt_from_request(locations=["headers", "cookies"], fresh=False)
    permission_validate(data[0])

    role = db.session.query(UserRole).filter_by(id=id).first()
    if not role:
        return HttpExceptions().not_exists("Role", id)

    db.session.delete(role)
    db.session.commit()

    resp = jsonify({"message": f"Role {role.id} deleted success"})
    return resp, 200


@jwt_required(True, locations=["headers", "cookies"])
@role_bp.route("/<uuid:id>", methods=["PUT"])
def update_role(id):
    data = _decode_jwt_from_request(locations=["headers", "cookies"], fresh=False)
    permission_validate(data[0])
    name_validate(request)

    role = db.session.query(UserRole).filter_by(id=id).first()
    if not role:
        return HttpExceptions().not_exists("Role", id)

    role.name = request.json["role_name"]
    db.session.commit()

    resp = jsonify({"message": f"Role {role.id} updated success"})
    return resp, 200
