import pytest
from fastapi.testclient import TestClient
from src.app import app, reset_activities


@pytest.fixture
def client():
    """Test client fixture for FastAPI app."""
    reset_activities()  # Reset to initial state before each test
    return TestClient(app)