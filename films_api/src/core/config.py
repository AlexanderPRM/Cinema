import os
from logging import config as logging_config

from core.logger import LOGGING
from fastapi import Query
from pydantic import BaseSettings

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class CommonQueryParams:
    def __init__(
        self,
        page_number: int | None = Query(default=1, ge=1),
        page_size: int | None = Query(default=10, ge=1, le=50),
    ):
        self.page_number = page_number
        self.page_size = page_size


class Settings(BaseSettings):
    PROJECT_NAME: str
    PROJECT_VERSION: str
    REDIS_HOST: str
    REDIS_PORT: str
    ELASTIC_HOST: str
    ELASTIC_PORT: str
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    JWT_SECRET: str
    AUTH_REDIS_HOST: str
    AUTH_REDIS_PORT: str

    class Config:
        case_sensitive = True
        env_file = "config.env"


config = Settings()
