from api.v1 import admin_handlers
from core.config import postgres_settings
from db import postgres
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

ADMIN_API_VERSION = "0.0.1"

app = FastAPI(
    title="Admin",
    description="API для модерации киносервиса",
    version=ADMIN_API_VERSION,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    postgres.postgres_ = postgres.PostgreSQL(postgres_settings.POSTGRESQL_URL)


@app.on_event("shutdown")
async def shutdown():
    await postgres.postgres_.conn.close()


app.include_router(
    admin_handlers.router,
    prefix="/api/v1/admin",
    tags=["Запросы на совершение платёжной операции"],
)
