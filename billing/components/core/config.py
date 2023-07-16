from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SUBSCRIPTIONS_TABLE: str
    JWT_SECRET: str
    JWT_ADMIN_ROLE: str
    POSTGRESQL_URL: str
    SUBSCRIPTIONS_USERS_TABLE: str
    TRANSACTIONS_LOG_TABLE: str

    class Config:
        case_sensitive = True
        env_file = "config.env"


class PostgreSQLSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    SUBSCRIPTIONS_USERS_TABLE: str

    class Config:
        case_sensitive = True
        env_file = "config.env"


config = Settings()
postgres_settings = PostgreSQLSettings()
