import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.routes.v1.user import router
from app.db.models import User, UserRole
from app.schemas.user import UserCreate
from app.main import app  # Assuming your FastAPI app is in app.main

# Add the router to the app for testing
app.include_router(router)

client = TestClient(app)

@pytest.fixture
def mock_db_session(mocker):
    # Mock the database session
    mock_session = MagicMock()
    mocker.patch("app.routes.user.SessionLocal", return_value=mock_session)
    return mock_session

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
    mock_user = User(**user_data)
    mock_db_session.query.return_value.filter.return_value.first.return_value = None  # No existing user
    mock_db_session.add.return_value = None
    mock_db_session.commit.return_value = None
    mock_db_session.refresh.return_value = mock_user

    # Act
    response = client.post("/users/register", json=user_data)

    # Assert
    assert response.status_code == 200
    assert response.json()["email"] == user_data["email"]
    assert response.json()["name"] == user_data["name"]

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
    response = client.post("/users/register", json=user_data)

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "User with this email already exists."

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
    response = client.post("/users/register", json=user_data)

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Email and password are required for non-AI trainers."