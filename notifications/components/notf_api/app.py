from core.config import project_settings
from db.rabbitmq import RabbitWorker
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title=project_settings.NOTF_PROJECT_NAME,
    description="API для работы с пользовательским контентом",
    version=project_settings.NOTF_PROJECT_VERSION,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    rabbit_worker = RabbitWorker()
    await rabbit_worker.get_connection()
    await rabbit_worker.make_queues()
    app.state.rabbit_worker = rabbit_worker


@app.on_event("shutdown")
async def shutdown():
    await app.state.rabbit_worker.close_connection()
