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
    PAYMENT_REDIRECT_URL: str
    AUTH_SERVICE_URL: str = Field(default="http://nginx/auth/")
    NOTIFICATION_SERVICE_URL: str = Field("http://notification_api:8001/api/v1/notify/send/")
    SUBSCRIBE_OFF_TEMPLATE_ID: str = Field(default="7403a28a-a2f2-4981-be53-104364e44447")
    SUBSCRIBE_ON_TEMPLATE_ID: str = Field(default="a28e491f-a722-47e6-a87b-cc6b7c225aff")

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
    PROVIDERS_IP_LIST: dict = Field(
        {
            "yookassa": [
                ipaddress.ip_network("185.71.76.0/27"),
                ipaddress.ip_network("185.71.77.0/27"),
                ipaddress.ip_network("77.75.153.0/25"),
                ipaddress.ip_network("77.75.156.11"),
                ipaddress.ip_network("77.75.156.35"),
                ipaddress.ip_network("77.75.154.128/25"),
                ipaddress.ip_network("2a02:5180::/32"),
            ],
        }
    )


rabbit_settings = RabbitMQSettings()
config = Settings()
postgres_settings = PostgreSQLSettings()
ip_white_list = ProvidersIPLists()
