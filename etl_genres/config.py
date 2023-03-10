from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    URI: str
    URI_LOAD_DATA: str

    class Config:
        case_sensitive = True
        env_file = "config.env"


settings = Settings()
