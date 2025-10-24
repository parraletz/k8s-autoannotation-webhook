from fastapi import FastAPI

from app.api.di import build_container
from app.api.routes.item import get_router


def create_app():
    app = FastAPI(title="Platform API Template", version="0.1.0")
    container = build_container()
    item_router = get_router(container)
    app.include_router(item_router)
    return app


app = create_app()
