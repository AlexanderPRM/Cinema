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

    def signup(self, email, password):
        email = self.normalize_email(email)
        try:
            validate_email(email)
        except EmailError:
            return abort(Response(json.dumps({"message": "Email is not correct."}), 422))
        if db.session.query(User).filter_by(email=email).first():
            return abort(Response(json.dumps({"message": f"User {email} already exists."}), 422))

        hashed_pass = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = User(email=email, password=hashed_pass)
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

    def change_password():
        pass

    def change_email():
        pass
