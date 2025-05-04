import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    payload = {
        "email": "testuser@athleo.ai",
        "password": "supersecure"
    }
    response = client.post("/users/register", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["email"] == payload["email"]