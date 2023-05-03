import logging

import uvicorn
from api import api_blueprint_v1
from api.v1.user_handlers import jwt
from core.config import config
from core.logger import LOGGING
from core.middleware import check_rate_limit
from db.postgres import db
from db.redis import redis_db
from flasgger import Swagger
from flask import Flask
from flask_migrate import Migrate

app = Flask(__name__)
migrate = Migrate(app, db)

app.register_blueprint(api_blueprint_v1)

with app.app_context():
    from cli.superuser import create_super_user  # noqa: 402

swagger = Swagger(app, template_file="openapi.yaml")


def init_redis(app: Flask):
    redis_host = config.AUTH_REDIS_HOST
    redis_port = config.AUTH_REDIS_PORT
    app.config["REDIS_HOST"] = redis_host
    app.config["REDIS_PORT"] = redis_port
    redis_db.init_app(app)


def init_jwt(app: Flask):
    secret_key = config.JWT_SECRET
    access_token_exp = config.ACCESS_TOKEN_EXPIRES
    refresh_token_exp = config.REFRESH_TOKEN_EXPIRES
    app.config["JWT_SECRET_KEY"] = secret_key
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = int(access_token_exp)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = int(refresh_token_exp)
    jwt.init_app(app)


def init_db(app: Flask):
    db_name = config.AUTH_POSTGRES_DB
    db_user = config.AUTH_POSTGRES_USER
    db_pass = config.AUTH_POSTGRES_PASSWORD
    db_host = config.AUTH_POSTGRES_HOST
    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}"
    db.init_app(app)


@app.before_request
def before_request():
    check_rate_limit()


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
