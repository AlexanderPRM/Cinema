import os
from logging import config as logging_config

from pydantic import BaseSettings

from core import logger

logging_config.dictConfig(logger.LOGGING)


class Settings(BaseSettings):
    AUTH_REDIS_HOST: str
    AUTH_REDIS_PORT: str
    AUTH_POSTGRES_USER: str
    AUTH_POSTGRES_PASSWORD: str
    AUTH_POSTGRES_HOST: str
    AUTH_POSTGRES_PORT: str
    AUTH_POSTGRES_DB: str
    JWT_SECRET: str
    ACCESS_TOKEN_EXPIRES: int
    REFRESH_TOKEN_EXPIRES: int
    MAX_TOKENS: int
    SEC_FOR_TOKEN: float
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    class Config:
        case_sensitive = True
        env_file = "config.env"


config = Settings()
