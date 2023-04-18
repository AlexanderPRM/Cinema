from core.permissions import superuser_required
from core.utils import is_uuid_valid
from db.models import User, UserRole
from db.postgres import db
from flask import Blueprint, Response, abort, json, jsonify, request
from services.exception_service import HttpExceptions
from services.role_service import RoleService

role_bp = Blueprint("role", __name__, url_prefix="/role")


def name_validate(request):
    if "role_name" not in request.json:
        return abort(Response(json.dumps({"error_message": "Name not specified"}), 422))


@role_bp.route("/", methods=["GET"])
@superuser_required
def get_roles():
    roles = db.session.query(UserRole).all()
    roles = [{"id": role.id, "name": role.name} for role in roles]

    resp = jsonify({"roles": roles})
    return resp, 200


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
    return resp, 201


@role_bp.route("/<uuid:id>", methods=["DELETE"])
@superuser_required
def delete_role(id):
    role = db.session.query(UserRole).filter_by(id=id).first()
    if not role:
        return HttpExceptions().not_exists("Role", id)

    db.session.delete(role)
    db.session.commit()

    resp = jsonify({"message": f"Role {role.id} deleted successfully"})
    return resp, 200


@role_bp.route("/<uuid:id>", methods=["PUT"])
@superuser_required
def update_role(id):
    name_validate(request)

    role = db.session.query(UserRole).filter_by(id=id).first()
    if not role:
        return HttpExceptions().not_exists("Role", id)

    role.name = request.json["role_name"]
    db.session.commit()

    resp = jsonify({"message": f"Role {role.id} updated successfully"})
    return resp, 200


@role_bp.route("/change_role/<uuid:id>", methods=["PUT"])
@superuser_required
def change_role(id):
    role_name = request.json["role_name"]
    if not is_uuid_valid(id):
        return HttpExceptions().not_valid_uuid()
    role = RoleService().get(role_name)
    if not role:
        return HttpExceptions().not_exists("Role", role_name)
    user = db.session.query(User).filter_by(id=id).first()
    if not user:
        return HttpExceptions().not_exists("User", id)
    RoleService().change_user_role(role=role, user=user)
    resp = jsonify({"message": f"{user.email}'s role updated to {role.name} successfully"})
    return resp, 200


@role_bp.route("/change_role_to_default/<uuid:id>", methods=["PUT"])
@superuser_required
def change_role_to_default(id):
    if not is_uuid_valid(id):
        return HttpExceptions().not_valid_uuid()
    user = db.session.query(User).filter_by(id=id).first()
    if not user:
        return HttpExceptions().not_exists("User", id)
    RoleService().change_user_role_to_default(user=user)
    resp = jsonify({"message": f"{user.email}'s role updated to default successfully"})
    return resp, 200
