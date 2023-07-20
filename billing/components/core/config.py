import ipaddress

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    JWT_SECRET: str
    JWT_ADMIN_ROLE: str
    REDIS_HOST: str
    REDIS_PORT: int
    YOOKASSA_SHOP_ID: str
    YOOKASSA_SHOP_SECRET: str
    # PAYMENT_REDIRECT_URL: str

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
    TRANSACTIONS_LOG_TABLE: str
    SUBSCRIPTIONS_USERS_TABLE: str
    SUBSCRIPTIONS_TABLE: str
    TRANSACTIONS_LOG_TABLE: str
    POSTGRESQL_URL: str

    class Config:
        case_sensitive = True
        env_file = "config.env"


class RabbitMQSettings(BaseSettings):
    BILLING_QUEUE_NOTIFICATIONS: str
    BILLING_QUEUE_AUTH: str
    BILLING_EXCHANGE: str
    RABBITMQ_USER: str
    RABBITMQ_PASS: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int

    class Config:
        case_sensitive = True
        env_file = "config.env"


class ProvidersIPLists(BaseSettings):
    PROVIDERS_IP_LIST: dict = Field({
        "yookassa": 
            [
                ipaddress.ip_network("185.71.76.0/27"),
                ipaddress.ip_network("185.71.77.0/27"),
                ipaddress.ip_network("77.75.153.0/25"),
                ipaddress.ip_network("77.75.156.11"),
                ipaddress.ip_network("77.75.156.35"),
                ipaddress.ip_network("77.75.154.128/25"),
                ipaddress.ip_network("2a02:5180::/32"),
            ],
    })


rabbit_settings = RabbitMQSettings()
config = Settings()
postgres_settings = PostgreSQLSettings()
ip_white_list = ProvidersIPLists()
