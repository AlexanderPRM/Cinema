from pydantic import BaseSettings, Field


class BaseConfig(BaseSettings):
    client_host_1: str = Field("clickhouse-node1", env="CLIENT_HOST_1")
    client_host_2: str = Field("clickhouse-node3", env="CLIENT_HOST_2")

    class Config:
        case_sensitive = False
        env_file = "config.env"


baseconfig = BaseConfig()
