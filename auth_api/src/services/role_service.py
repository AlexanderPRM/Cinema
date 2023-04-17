from db.models import ServiceUser, UserRole
from db.postgres import db


class RoleService:
    def __init__(self):
        pass

    def get(self, name):
        return db.session.query(UserRole).filter_by(name=name).first()

    def post(self, name):
        role = UserRole(name=name)
        db.session.add(role)
        db.session.commit()
        return role

    def change_user_role(self, role, user):
        user.role = role
        db.session.commit()
        return role

    def change_user_role_to_default(self, user):
        role_service = RoleService()
        role = role_service.get("default")
        if not role:
            role = role_service.post("default")
        user_service = db.session.query(ServiceUser).filter_by(user=user).first()
        if user_service:
            user_service.role = role
        else:
            user_service = ServiceUser(user=user, role=role)
            db.session.add(user_service)
        db.session.commit()
        return role
