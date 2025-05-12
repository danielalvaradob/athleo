"""
This file defines shared pytest fixtures for the test suite in this directory and its subdirectories.

Why do we need this file?
- `conftest.py` is a special file recognized by pytest to provide reusable fixtures.
- By defining common fixtures like `mock_db_session` here, we avoid duplicating code across multiple test files.
- This ensures that all test files in the `routes/v1/` directory and its subdirectories can use the `mock_db_session` fixture without needing to redefine it.
- It adheres to the DRY (Don't Repeat Yourself) principle and improves maintainability.
- If the logic for mocking the database session changes, we only need to update it in this file.

New engineers can use this file to define additional shared fixtures for tests in this directory structure.
"""

import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_db_session(mocker):
    # Mock the database session
    mock_session = MagicMock()
    mocker.patch("app.db.session.SessionLocal", return_value=mock_session)
    return mock_session