import bcrypt
from db.models import ServiceUser, User
from db.postgres import db
from pydantic import EmailError, validate_email

from .exception_service import HttpExceptions
from .role_service import RoleService


class UserService:
    def __init__(self):
        pass

    @classmethod
    def normalize_email(self, email):
        email_user, email_domain = email.lower().strip().split("@")
        if "+" in email_user:
            email_user = email_user[: email_user.find("+")]
        return f"{email_user}@{email_domain}"

    def signin():
        pass

    def signup(self, email, password, name):
        exceptions = HttpExceptions()
        try:
            validate_email(email)
        except EmailError:
            return exceptions.already_exists("User", email)
        email = self.normalize_email(email)
        if db.session.query(User).filter_by(email=email).first():
            return exceptions.email_error()

        hashed_pass = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = User(email=email, password=hashed_pass.decode(), name=name)
        db.session.add(user)
        db.session.commit()
        role_service = RoleService()
        role = role_service.change_user_role_to_default(user=user)
        return email, password, role, user

    def change_password():
        pass

    def change_email():
        pass
