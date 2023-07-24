from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    PAYMENT_API_URL: str
    ADMIN_API_URL: str
    BILLING_API_URL: str
    JWT_SECRET: str

    class Config:
        case_sensitive = False
        env_file = "config_tests.env"


baseconfig = BaseConfig()
