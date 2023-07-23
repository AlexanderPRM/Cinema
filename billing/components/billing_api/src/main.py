from api.v1 import billing
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

BILLING_API_VERSION = "0.0.1"


app = FastAPI(
    title="Billing",
    description="API для работы с пользовательским контентом",
    version=BILLING_API_VERSION,
    docs_url="/openapi",
    openapi_url="/openapi.json",
    root_path="/billing_api",
    default_response_class=ORJSONResponse,
)

app.include_router(
    billing.router,
    prefix="/v1/billing",
    tags=["Запросы на совершение платёжной операции"],
)
