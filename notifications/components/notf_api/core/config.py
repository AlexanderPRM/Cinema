from pydantic import BaseSettings, Field


class PostgreSQLSettings(BaseSettings):
    NOTF_POSTGRES_DB: str
    NOTF_POSTGRES_HOST: str
    NOTF_POSTGRES_PORT: str
    NOTF_POSTGRES_USER: str
    NOTF_POSTGRES_PASSWORD: str
    POSTGRES_SUBSCRIBE_TABLE: str = Field("user_mailing_subscribe")

    class Config:
        case_sensitive = True
        env_file = "notf.env"


class ProjectSettings(BaseSettings):
    NOTF_PROJECT_NAME: str
    NOTF_PROJECT_VERSION: str
    JWT_SECRET: str

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


postgres_settings = PostgreSQLSettings()
project_settings = ProjectSettings()
rabbit_settings = RabbiMQSettings()
