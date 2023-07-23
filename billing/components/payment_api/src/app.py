from contextlib import asynccontextmanager

from db.rabbitmq import RabbitWorker
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

PAYMENT_PROJECT_NAME = "payment_service"
PAYMENT_PROJECT_VERSION = "0.0.1"


@asynccontextmanager
async def lifespan(app: FastAPI):
    rabbit_worker = RabbitWorker()
    await rabbit_worker.get_connection()
    await rabbit_worker.make_queues()
    app.state.rabbit_worker = rabbit_worker
    yield
    await app.state.rabbit_worker.close_connection()


app = FastAPI(
    title=PAYMENT_PROJECT_NAME,
    description="API для обработки платежей",
    version=PAYMENT_PROJECT_VERSION,
    docs_url="/openapi",
    openapi_url="/openapi.json",
    root_path="/payment_api",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)
