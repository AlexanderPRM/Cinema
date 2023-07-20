from api.v1 import payment
from main import app

app.include_router(
    payment.router,
    prefix="/api/v1/provider",
    tags=["Работа с провайдерами"],
)
