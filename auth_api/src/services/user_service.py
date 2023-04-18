from datetime import datetime

import bcrypt
from db.models import ServiceUser, User, UserLoginHistory, UserRole
from db.postgres import db
from pydantic import EmailError, validate_email

from .exception_service import HttpExceptions
from .role_service import RoleService


class UserService:
    @classmethod
    def normalize_email(self, email):
        email_user, email_domain = email.lower().strip().split("@")
        if "+" in email_user:
            email_user = email_user[: email_user.find("+")]
        return f"{email_user}@{email_domain}"

    def signin(self, email, password, useragent):
        try:
            validate_email(email)
        except EmailError:
            return HttpExceptions().email_error()
        email = self.normalize_email(email)
        user = db.session.query(User).filter_by(email=email).first()
        if not user:
            return HttpExceptions().not_exists("User", email)

        if bcrypt.checkpw(password.encode(), user.password.encode()):
            role = (
                db.session.query(UserRole)
                .join(ServiceUser)
                .filter(ServiceUser.user == user)
                .first()
            )
            login_record = UserLoginHistory(
                authentication_date=datetime.utcnow(), user_id=user.id, user_agent=useragent
            )
            db.session.add(login_record)
            db.session.commit()
            return email, role, user
        else:
            return HttpExceptions().password_error()

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
        if role := role_service.get("default"):
            user_service = ServiceUser(user=user, role=role)
            db.session.add(user_service)
            db.session.commit()
        else:
            role = role_service.post("default")
            user_service = ServiceUser(user=user, role=role)
            db.session.add(user_service)
            db.session.commit()
        return email, password, role, user

    def change_password():
        pass

    def change_email():
        pass

    def login_history(self, email):
        user_id = db.session.query(User.id).filter_by(email=email).scalar()
        return (
            db.session.query(UserLoginHistory)
            .join(User, User.id == UserLoginHistory.user_id)
            .filter(User.id == user_id)
            .all()
        )
