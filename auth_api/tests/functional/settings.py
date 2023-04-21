from pydantic import BaseSettings, Field


class BaseConfig(BaseSettings):
    service_url: str = Field("http:/127.0.0.1:8000", env="SERVICE_URL")

    class Config:
        case_sensitive = False
        env_file = "config_tests.env"


baseconfig = BaseConfig()
