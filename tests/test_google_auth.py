import pytest
from flask import session
from unittest.mock import patch, MagicMock
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@patch("app.controllers.auth.firebase_auth.verify_id_token")
@patch("app.controllers.auth.FirebaseUserRepository")
def test_google_login_existing_user(mock_repo_class, mock_verify_token, client):
    mock_verify_token.return_value = {
        "uid": "abc123",
        "email": "test@example.com",
        "name": "Test User"
    }

    mock_repo = MagicMock()
    mock_repo.get_user_by_email.return_value = {
        "id": 1,
        "role": "Student",
        "email": "test@example.com",
        "name": "Test User",
        "status": "active"
    }
    mock_repo_class.return_value = mock_repo

    response = client.post("/auth/google-login", json={"token": "fake-token"})

    assert response.status_code == 200
    assert response.json["message"] == "Login con Google exitoso"



@patch("app.controllers.auth.firebase_auth.verify_id_token")
@patch("app.controllers.auth.FirebaseUserRepository")
def test_google_login_new_user(mock_repo_class, mock_verify_token, client):
    mock_verify_token.return_value = {
        "uid": "xyz999",
        "email": "newuser@example.com",
        "name": "New User"
    }

    mock_repo = MagicMock()
    mock_repo.get_user_by_email.return_value = None


    mock_repo.add_user.return_value = {
        "id": 2,
        "role": "Student",
        "email": "newuser@example.com",
        "name": "New User",
        "status": "pending"
    }

    mock_repo_class.return_value = mock_repo

    response = client.post("/auth/google-login", json={"token": "fake-token"})

    mock_repo.add_user.assert_called_once_with(
        name="New User",
        email="newuser@example.com",
        password=None,
        role="Student"
    )

    assert response.status_code == 200
    assert response.json["message"] == "Login con Google exitoso"

