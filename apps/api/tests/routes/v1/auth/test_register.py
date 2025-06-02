import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.routes.v1.auth.register import router
from app.db.models.user import User
from app.main import app  # Assuming your FastAPI app is in app.main

# Add the router to the app for testing
app.include_router(router)
client = TestClient(app)

def test_register_valid_user(mock_db_session):
    # Arrange
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "password": "securepassword",
        "role": "user",
        "language": "en",
        "is_ai_trainer": False,
    }
    mock_db_session.query.return_value.filter.return_value.first.return_value = None  # No existing user
    mock_db_session.add.return_value = None
    mock_db_session.commit.return_value = None
    mock_db_session.refresh.return_value = User(**user_data)

    # Act
    response = client.post("/auth/register", json=user_data)

    # Assert
    assert response.status_code == 200
    assert response.json()["email"] == user_data["email"]
    assert response.json()["name"] == user_data["name"]

def test_register_missing_email(mock_db_session):
    # Arrange
    user_data = {
        "name": "Test User",
        "password": "securepassword",
        "role": "user",
        "language": "en",
        "is_ai_trainer": False,
    }

    # Act
    response = client.post("/auth/register", json=user_data)

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Email and password are required for non-AI trainers."

def test_register_duplicate_email(mock_db_session):
    # Arrange
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "password": "securepassword",
        "role": "user",
        "language": "en",
        "is_ai_trainer": False,
    }
    mock_db_session.query.return_value.filter.return_value.first.return_value = User(**user_data)  # Existing user

    # Act
    response = client.post("/auth/register", json=user_data)

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "User with this email already exists."