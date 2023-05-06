from datetime import datetime

import bcrypt
from pydantic import EmailError, validate_email

from core.utils import check_device_type, normalize_email
from db.models import ServiceUser, User, UserLoginHistory, UserRole
from db.postgres import db
from .exception_service import HttpExceptions
from .role_service import RoleService


class UserService:
    def add_login_history(self, user_id, useragent):
        device_type = check_device_type(useragent)
        login_record = UserLoginHistory(
            authentication_date=datetime.utcnow(),
            user_id=user_id,
            user_agent=useragent,
            device_type=device_type,
        )
        db.session.add(login_record)
        db.session.commit()
        return login_record

    def signin(self, email, password, useragent):
        try:
            validate_email(email)
        except EmailError:
            return HttpExceptions().email_error()
        email = normalize_email(email)
        user = db.session.query(User).filter_by(email=email).first()
        if not user:
            return HttpExceptions().not_exists("User", email)

        if bcrypt.checkpw(password.encode(), user.password.encode()):
            role = self.get_user_role(user)
            self.add_login_history(user_id=user.id, useragent=useragent)
            return email, role, user
        return HttpExceptions().password_error()

    def signup(self, email, password, name, useragent):
        exceptions = HttpExceptions()
        try:
            validate_email(email)
        except EmailError:
            return exceptions.already_exists("User", email)
        email = normalize_email(email)
        if db.session.query(User).filter_by(email=email).first():
            return exceptions.email_error()

        hashed_pass = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = User(email=email, password=hashed_pass.decode(), name=name)
        db.session.add(user)
        db.session.commit()
        role_service = RoleService()
        role = role_service.change_user_role_to_default(user=user)
        self.add_login_history(user_id=user.id, useragent=useragent)
        return email, password, role, user

    def refresh(self, email):
        user = User.query.filter_by(email=email).first()
        return user.id

    def login_history(self, email, page_size, page_number):
        user_id = db.session.query(User.id).filter_by(email=email).scalar()
        pagination = (
            db.session.query(UserLoginHistory)
            .join(User, User.id == UserLoginHistory.user_id)
            .filter(User.id == user_id)
            .paginate(page=page_number, per_page=page_size, error_out=False)
        )
        return pagination.items

    def get_profile_info(self, email):
        user = User.query.filter_by(email=email).first()
        return user

    def change_name(self, email, new_name):
        db.session.query(User).filter(User.email.ilike(email)).update(
            {"name": new_name}, synchronize_session="fetch"
        )
        db.session.commit()

    def check_password(self, email, password):
        cur_hash_password = User.query.filter_by(email=email).first().password
        return bcrypt.checkpw(password.encode(), cur_hash_password.encode())

    def change_password(self, email, password):
        hash_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        db.session.query(User).filter(User.email.ilike(email)).update(
            {"password": hash_password.decode()}, synchronize_session="fetch"
        )
        db.session.commit()

    def change_email(self, email, new_email):
        db.session.query(User).filter(User.email.ilike(email)).update(
            {"email": new_email}, synchronize_session="fetch"
        )
        db.session.commit()

    def get_user_role(self, user):
        role = db.session.query(UserRole).join(ServiceUser).filter(ServiceUser.user == user).first()
        return role
