from flask import Blueprint

from .v1.user_handlers import user_bp

api_blueprint_v1 = Blueprint("api", __name__, url_prefix="/api/v1")

api_blueprint_v1.register_blueprint(user_bp)
