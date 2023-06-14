import logging

import uvicorn
from api.v1.notify import router
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


@app.on_event('startup')
async def startup():
    await RabbitWorker().make_queues()


app.include_router(router, prefix="/api/v1/notify")


if __name__ == "__main__":
    uvicorn.run("main:app", port=8009, log_level=logging.DEBUG)
