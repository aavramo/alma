import pytest

from api import app


@pytest.fixture
def client():
    from fastapi.testclient import TestClient

    yield TestClient(app)
