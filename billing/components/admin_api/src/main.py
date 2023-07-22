from api.v1 import admin_handlers
from core.config import postgres_settings, rabbit_settings
from db import postgres, rabbit
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

ADMIN_API_VERSION = "0.0.1"

app = FastAPI(
    title="Admin",
    description="API для модерации сервиса оплаты.",
    version=ADMIN_API_VERSION,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    postgres.postgres_ = postgres.PostgreSQL(postgres_settings.POSTGRESQL_URL)
    rabbit.rabbit_ = rabbit.RabbitMQBroker(
        url=f"amqp://{rabbit_settings.RABBITMQ_USER}:{rabbit_settings.RABBITMQ_PASS}@"
        f"{rabbit_settings.RABBITMQ_HOST}/",
        queue_name=rabbit_settings.BILLING_QUEUE_NOTIFICATIONS,
    )
    await rabbit.rabbit_.connect()


@app.on_event("shutdown")
async def shutdown():
    await postgres.postgres_.conn.close()
    await rabbit.rabbit_.disconnect()


app.include_router(
    admin_handlers.router,
    prefix="/api/v1/admin",
    tags=["Запросы на совершение платёжной операции"],
)
