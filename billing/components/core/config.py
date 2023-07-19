from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SUBSCRIPTIONS_TABLE: str
    JWT_SECRET: str
    JWT_ADMIN_ROLE: str
    POSTGRESQL_URL: str
    SUBSCRIPTIONS_USERS_TABLE: str
    TRANSACTIONS_LOG_TABLE: str
    REDIS_HOST: str
    REDIS_PORT: int
    YOOKASSA_SHOP_ID: str
    YOOKASSA_SHOP_SECRET: str

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


class RabbitMQSettings(BaseSettings):
    BILLING_QUEUE_NOTIFICATIONS: str
    BILLING_QUEUE_AUTH: str
    RABBITMQ_USER: str
    RABBITMQ_PASS: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int

    class Config:
        case_sensitive = True
        env_file = "config.env"


rabbit_settings = RabbitMQSettings()
config = Settings()
postgres_settings = PostgreSQLSettings()
