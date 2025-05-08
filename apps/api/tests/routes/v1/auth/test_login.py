import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.routes.v1.auth.login import router
from app.db.models import User
from app.main import app  # Assuming your FastAPI app is in app.main

# Add the router to the app for testing
app.include_router(router)
client = TestClient(app)

@pytest.fixture
def mock_jwt_functions(mocker):
    # Mock JWT functions
    mocker.patch("app.routes.v1.auth.login.create_access_token", return_value="mock_access_token")
    mocker.patch("app.routes.v1.auth.login.create_refresh_token", return_value="mock_refresh_token")
    mocker.patch("app.routes.v1.auth.login.decode_token", return_value={"sub": "mock_user_id"})

def test_login_valid_user(mock_db_session, mock_jwt_functions):
    # Arrange
    user_data = {
        "id": "mock_user_id",
        "email": "test@example.com",
        "password_hash": "hashed_password",
        "name": "Test User",
        "role": "user",
        "is_ai_trainer": False,
        "language": "en",
    }
    mock_user = User(**user_data)
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_user

    # Act
    response = client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "password"}
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["access_token"] == "mock_access_token"
    assert response.cookies.get("refresh_token") == "mock_refresh_token"

def test_login_invalid_user(mock_db_session):
    # Arrange
    mock_db_session.query.return_value.filter.return_value.first.return_value = None

    # Act
    response = client.post(
        "/auth/login",
        data={"username": "invalid@example.com", "password": "password"}
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid email or password."

def test_refresh_valid_token(mock_db_session, mock_jwt_functions):
    # Arrange
    user_data = {
        "id": "mock_user_id",
        "email": "test@example.com",
        "password_hash": "hashed_password",
        "name": "Test User",
        "role": "user",
        "is_ai_trainer": False,
        "language": "en",
    }
    mock_user = User(**user_data)
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_user

    # Act
    response = client.post(
        "/auth/refresh",
        cookies={"refresh_token": "mock_refresh_token"}
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["access_token"] == "mock_access_token"

def test_refresh_invalid_token(mock_db_session, mocker):
    # Arrange
    mocker.patch("app.routes.v1.auth.login.decode_token", side_effect=Exception("Invalid or expired token"))

    # Act
    response = client.post(
        "/auth/refresh",
        cookies={"refresh_token": "invalid_refresh_token"}
    )

    # Assert
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid refresh token."