import logging

import uvicorn
from core.config import config
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title=config.UGC_PROJECT_NAME,
    description="Отслеживание прогресса просмотра фильма",
    version=config.UGC_PROJECT_VERSION,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8010, log_level=logging.DEBUG)
