import logging

import uvicorn
from api.v1.payment import router
from app import app

app.include_router(
    router,
    prefix="/api/v1/provider",
    tags=["Работа с провайдерами"],
)


if __name__ == "__main__":
    uvicorn.run("app:app", port=8000, log_level=logging.DEBUG)
