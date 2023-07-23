from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    PAYMENT_API_URL: str
    JWT_SECRET: str

    class Config:
        case_sensitive = False
        env_file = "config.env"


baseconfig = BaseConfig()
