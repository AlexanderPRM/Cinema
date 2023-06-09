from pydantic import BaseSettings, Field


class BaseConfig(BaseSettings):
    service_url: str = Field(env="SERVICE_URL", default="http://functional-ugc2-1:8000/api/v1/")
    jwt_secret: str = Field(env="JWT_SECRET")

    class Config:
        case_sensitive = False
        env_file = "config_tests.env"


baseconfig = BaseConfig()
