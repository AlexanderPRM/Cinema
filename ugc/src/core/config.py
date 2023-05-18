from pydantic import BaseSettings


class UGCSettings(BaseSettings):
    UGC_PROJECT_NAME: str
    UGC_PROJECT_VERSION: str

    class Config:
        case_sensitive = True
        env_file = "config.env"


class KafkaSettings(BaseSettings):
    BOOTSTRAP_SERVERS: list

    class Config:
        case_sensitive = True
        env_file = "config.env"


config = UGCSettings()
kafka_config = KafkaSettings()
