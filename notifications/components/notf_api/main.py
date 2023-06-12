from core.config import project_settings
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
