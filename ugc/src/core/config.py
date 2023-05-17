from pydantic import BaseSettings


class UGCSettings(BaseSettings):
    UGC_PROJECT_NAME: str
    UGC_PROJECT_VERSION: str

    class Config:
        case_sensitive = True
        env_file = "config.env"


config = UGCSettings()
