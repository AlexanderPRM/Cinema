import logging

import uvicorn
from api.v1.notify import router
from app import app

app.include_router(router, prefix="/api/v1/notify")

if __name__ == "__main__":
    uvicorn.run("app:app", port=8009, log_level=logging.DEBUG)
