from fastapi import FastAPI

from app.api.di import build_container
from app.api.routes.webhook import get_router as get_webhook_router


def create_app():
    app = FastAPI(title="Platform API Template", version="0.1.0")
    container = build_container()
    webhook_router = get_webhook_router(container)
    app.include_router(webhook_router)
    return app


app = create_app()
