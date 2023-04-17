from db.models import UserRole
from db.postgres import db


class RoleService:
    def __init__(self):
        pass

    def get(self, name):
        return db.session.query(UserRole).filter_by(name=name).first()

    def post(name):
        role = UserRole(name=name)
        db.session.add(role)
        db.session.commit()
        return role
