import logging

import redis
import uvicorn
from api.v1.user_handlers import jwt, user_bp
from core.config import config
from core.logger import LOGGING
from db.postgres import db
from flask import Flask

app = Flask(__name__)
app.config

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
    redis_host = config.AUTH_REDIS_HOST
    redis_port = config.AUTH_REDIS_PORT
    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}"
    app.config["REDIS_URL"] = f"redis://{redis_host}:{redis_port}/0"
    db.init_app(app)
    with app.app_context():
        # Импорты моделей для создания в БД.
        from db.models import ServiceUser, User, UserLoginHistory, UserRole  # noqa:402

        db.create_all()


if __name__ == "__main__":
    init_jwt(app)
    init_db(app)
    app.run()
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
