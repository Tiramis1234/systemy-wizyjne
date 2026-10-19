import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client() -> TestClient:
    """A fresh application (with empty state) for every test."""
    return TestClient(create_app())
