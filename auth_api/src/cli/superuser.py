import bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token
from pydantic import EmailError, validate_email

from app import app
from core import config
from services.role_service import RoleService
from db.models import ServiceUser, User
from db.postgres import db
from db.redis import redis_db


@app.cli.command("create-superuser")
def create_super_user():
    """Create superuser"""
    while True:
        try:
            email = input("Enter your email: ")
            if db.session.query(User).filter_by(email=email).first():
                print(f"User {email} already exists.")
                exit()
            validate_email(email)
            break
        except EmailError:
            print("\nPlease enter the correct email")
        except KeyboardInterrupt:
            exit()
    password = input("Enter your password: ")
    hashed_pass = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    user = User(email=email, password=hashed_pass.decode())
    db.session.add(user)
    db.session.commit()
    role_service = RoleService()
    if role := role_service.get("superuser"):
        user_service = ServiceUser(user=user, role=role)
        db.session.add(user_service)
        db.session.commit()
    else:
        role = role_service.post("superuser")
        user_service = ServiceUser(user=user, role=role)
        db.session.add(user_service)
        db.session.commit()
    access_token = create_access_token(identity=email, additional_claims={"role": "superuser"})
    refresh_token = create_refresh_token(identity=email)
    redis_db.setex(
        str(user.id) + "_" + "admin-pc" + "_refresh",
        config.config.REFRESH_TOKEN_EXPIRES,
        refresh_token,
    )
    print("\nNow creating superuser:", email)
    print(f"Your access_token: \n{access_token}")
    print(f"\nYour refresh_token: \n{refresh_token}")
