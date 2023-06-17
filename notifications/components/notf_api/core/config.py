from pydantic import BaseSettings


class ProjectSettings(BaseSettings):
    NOTF_PROJECT_NAME: str
    NOTF_PROJECT_VERSION: str

    class Config:
        case_sensitive = True
        env_file = "config.env"


class RabbiMQSettings(BaseSettings):
    NOTF_RABBITMQ_HOST: str
    NOTF_RABBITMQ_PORT: str
    NOTF_RABBITMQ_USER: str
    NOTF_RABBITMQ_PASS: str
    EMAIL_EXCHANGE: str
    EMAIL_QUEUE: str

    class Config:
        case_sensitive = True
        env_file = "config.env"


project_settings = ProjectSettings()
rabbit_settings = RabbiMQSettings()
