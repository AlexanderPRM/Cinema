from pydantic import BaseSettings


class ProjectSettings(BaseSettings):
    NOTF_PROJECT_NAME: str
    NOTF_PROJECT_VERSION: str

    class Config:
        case_sensitive = True
        env_file = "config.env"


class RabbiMQSettings(BaseSettings):
    RABBITMQ_HOST: str
    RABBITMQ_PORT: str
    RABBITMQ_USER: str
    RABBITMQ_PASS: str
    EMAIL_EXCHANGE: str
    EMAIL_QUEUE: str

    class Config:
        case_sensitive = True
        env_file = "config.env"


project_settings = ProjectSettings()
rabbit_settings = RabbiMQSettings()
