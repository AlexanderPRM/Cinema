import os
from logging import config as logging_config

from core import logger
from pydantic import BaseSettings, Field

logging_config.dictConfig(logger.LOGGING)


class GoogleSettings(BaseSettings):
    GOOGLE_FILE: str
    GOOGLE_REDIRECT_URI: str

    class Config:
        case_sensitive = True
        env_file = "config.env"


class YandexSettings(BaseSettings):
    YANDEX_CLIENT_ID: str
    YANDEX_CLIENT_SECRET: str
    YANDEX_REDIRECT_URI: str

    class Config:
        case_sensitive = True
        env_file = "config.env"


class Settings(BaseSettings):
    AUTH_REDIS_HOST: str
    AUTH_REDIS_PORT: str
    AUTH_POSTGRES_USER: str
    AUTH_POSTGRES_PASSWORD: str
    AUTH_POSTGRES_HOST: str
    AUTH_POSTGRES_PORT: str
    AUTH_POSTGRES_DB: str
    JWT_SECRET: str
    TRACER: str
    ACCESS_TOKEN_EXPIRES: int
    REFRESH_TOKEN_EXPIRES: int
    MAX_TOKENS: int
    SEC_FOR_TOKEN: float
    RATE_LIMIT_ENABLED: bool
    URL_SAFE_SERIALIZER_SECRET: str
    URL_SAFE_SERIALIZER_SALT: str
    NOTIFICATION_SERVICE_URL: str = Field("http://notification_api:8001/api/v1/notify/send/")
    WELCOME_TEMPLATE_ID: str = Field("5a4fd7c0-8cef-44f5-a16d-0f78f72b0897")
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    class Config:
        case_sensitive = True
        env_file = "config.env"


config = Settings()
yandex_config = YandexSettings()
google_config = GoogleSettings()
