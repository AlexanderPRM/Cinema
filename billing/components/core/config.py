from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    JWT_SECRET: str
    JWT_ADMIN_ROLE: str
    YOOKASSA_SHOP_ID: int
    YOOKASSA_SHOP_SECRET: str
    PAYMENT_REDIRECT_URL: str

    class Config:
        case_sensitive = True
        env_file = "config.env"


class PostgreSQLSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    POSTGRESQL_URL: str
    SUBSCRIPTIONS_TABLE: str
    SUBSCRIPTIONS_USERS_TABLE: str
    TRANSACTIONS_LOG_TABLE: str

    class Config:
        case_sensitive = True
        env_file = "config.env"


config = Settings()
postgres_settings = PostgreSQLSettings()
