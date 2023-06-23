from pydantic import BaseSettings, Field


class WorkerSettings(BaseSettings):
    JWT_SECRET: str
    JWT_ADMIN_ROLE: str
    NOTF_ELASTICEMAIL_API_KEY: str
    NOTF_ELASTICEMAIL_FROM_EMAIL: str
    AUTH_URL: str = Field("http://nginx/auth/api/v1/user/")

    class Config:
        case_sensitive = True
        env_file = "notf.env"


class PostgreSQLSettings(BaseSettings):
    NOTF_POSTGRES_DB: str
    NOTF_POSTGRES_HOST: str
    NOTF_POSTGRES_PORT: str
    NOTF_POSTGRES_USER: str
    NOTF_POSTGRES_PASSWORD: str
    TEMPLATE_TABLE: str = Field("templates")
    POSTGRES_SUBSCRIBE_TABLE: str = Field("user_mailing_subscribe")

    class Config:
        case_sensitive = True
        env_file = "notf.env"


class RabbiMQSettings(BaseSettings):
    NOTF_RABBITMQ_HOST: str
    NOTF_RABBITMQ_PORT: str
    NOTF_RABBITMQ_USER: str
    NOTF_RABBITMQ_PASS: str
    EMAIL_EXCHANGE: str
    EMAIL_QUEUE: str

    class Config:
        case_sensitive = True
        env_file = "notf.env"


rabbit_settings = RabbiMQSettings()
postgres_settings = PostgreSQLSettings()
worker_setting = WorkerSettings()
