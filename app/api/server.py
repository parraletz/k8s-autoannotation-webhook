"""Server entry point"""

from fastapi import FastAPI

from app import __description__, __name__, __version__
from app.api.di import build_container
from app.api.routes.webhook import get_router as get_webhook_router


def create_app() -> FastAPI:
    app = FastAPI(title=__name__, version=__version__, description=__description__)
    container = build_container()
    webhook_router = get_webhook_router(container)
    app.include_router(webhook_router)
    return app


app = create_app()
