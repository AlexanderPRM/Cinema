import logging

import bcrypt
import uvicorn
from api.v1.user_handlers import jwt, user_bp
from core.config import config
from core.logger import LOGGING
from db.postgres import db
from db.redis import redis_db
from flask import Flask
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_migrate import Migrate
from pydantic import EmailError, validate_email

app = Flask(__name__)
migrate = Migrate(app, db)

app.register_blueprint(user_bp)


def init_jwt(app: Flask):
    secret_key = config.JWT_SECRET
    access_token_exp = config.ACCESS_TOKEN_EXPIRES
    refresh_token_exp = config.REFRESH_TOKEN_EXPIRES
    app.config["JWT_SECRET_KEY"] = secret_key
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = int(access_token_exp)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = int(refresh_token_exp)
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
    app.config["JWT_REFRESH_COOKIE_PATH"] = "/user/refresh"
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    app.config["JWT_BLACKLIST_ENABLED"] = True
    app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
    jwt.init_app(app)


def init_db(app: Flask):
    db_name = config.AUTH_POSTGRES_DB
    db_user = config.AUTH_POSTGRES_USER
    db_pass = config.AUTH_POSTGRES_PASSWORD
    db_host = config.AUTH_POSTGRES_HOST
    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}"
    db.init_app(app)


def init_redis(app: Flask):
    redis_host = config.AUTH_REDIS_HOST
    redis_port = config.AUTH_REDIS_PORT
    app.config["REDIS_HOST"] = redis_host
    app.config["REDIS_PORT"] = redis_port
    redis_db.init_app(app)


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
    role = db.session.query(UserRole).filter_by(name="superuser").first()
    if role:
        user_service = ServiceUser(user=user, role=role)
        db.session.add(user_service)
        db.session.commit()
    else:
        role = UserRole(name="superuser")
        user_service = ServiceUser(user=user, role=role)
        db.session.add(role)
        db.session.add(user_service)
        db.session.commit()
    refresh_token = create_access_token(identity=email, additional_claims={"role": "superuser"})
    access_token = create_refresh_token(identity=email)
    print("\nNow creating superuser:", email)
    print(f"Your access_token: \n{access_token}")
    print(f"\nYour refresh_token: \n{refresh_token}")


if __name__ == "__main__":
    init_jwt(app)
    init_db(app)
    init_redis(app)

    # Для разработки.
    app.run()
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
