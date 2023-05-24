from pydantic import BaseSettings


class UGCSettings(BaseSettings):
    UGC_PROJECT_NAME: str
    UGC_PROJECT_VERSION: str
    JWT_SECRET: str
    UGC_REDIS_HOST: str
    UGC_REDIS_PORT: str
    FILM_WATCH_TIME_EXPIRED: str
    UGC_ETL_REDIS_HOST: str
    UGC_ETL_REDIS_PORT: int

    class Config:
        case_sensitive = True
        env_file = "config.env"


class KafkaSettings(BaseSettings):
    BOOTSTRAP_SERVERS: list

    class Config:
        case_sensitive = True
        env_file = "config.env"


class ClickHouseSettings(BaseSettings):
    CLICKHOUSE_HOST: str
    CLICKHOUSE_PORT: int
    CLICKHOUSE_NODE_1: str
    CLICKHOUSE_TABLE_NAME: str

    class Config:
        case_sensitive = True
        env_file = "config.env"


config = UGCSettings()
kafka_config = KafkaSettings()
ch_config = ClickHouseSettings()
