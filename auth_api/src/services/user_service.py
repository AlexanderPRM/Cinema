import bcrypt
from db.models import ServiceUser, User, UserRole
from db.postgres import db
from flask import Response, abort, json
from pydantic import EmailError, validate_email


class UserService:  # Унаследовать надо будет
    def __init__(self):
        # super().__init__(self)
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
        try:
            validate_email(email)
        except EmailError:
            return abort(Response(json.dumps({"message": "Email is not correct."}), 422))
        email = self.normalize_email(email)
        if db.session.query(User).filter_by(email=email).first():
            return abort(Response(json.dumps({"message": f"User {email} already exists."}), 422))

        hashed_pass = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = User(email=email, password=hashed_pass.decode(), name=name)
        db.session.add(user)
        db.session.commit()
        role = db.session.query(UserRole).filter_by(name="default").first()
        if role:
            user_service = ServiceUser(user=user, role=role)
            db.session.add(user_service)
            db.session.commit()
        else:
            role = UserRole(name="default")
            user_service = ServiceUser(user=user, role=role)
            db.session.add(role)
            db.session.add(user_service)
            db.session.commit()
        return email, password, role, user

    def refresh(self, email):
        user = User.query.filter_by(email=email).first()
        return user.id

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
