from pydantic import BaseSettings, Field


class VerticaConfig(BaseSettings):
    vertica_host: str = Field(env="VERTICA_HOST", default="vertica-vertica-1")
    vertica_port: str = Field(env="VERTICA_PORT", default="5433")
    vertica_user: str = Field(env="VERTICA_USER", default="dbadmin")
    vertica_password: str = Field(env="VERTICA_PASSWORD", default="")
    vertica_db: str = Field(env="VERTICA_DB", default="docker")
    vertica_autocommit: bool = Field(env="VERTICA_AUTOCOMMIT", default="True")

    class Config:
        env_file = "config.env"


vertica_config = VerticaConfig()
