import pytest
from fastapi.testclient import TestClient

from app.api.di import build_container
from app.api.server import create_app


@pytest.fixture()
def container():
    return build_container(reset=True)


@pytest.fixture()
def app(container):
    return create_app()


@pytest.fixture()
def client(app):
    return TestClient(app)
