import pytest
from flask import session
from unittest.mock import patch, MagicMock
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@patch("app.controllers.auth.AuthStateContext.get_state")
@patch("app.controllers.auth.FirebaseUserRepository")
def test_google_login_existing_user(mock_repo_class, mock_get_state, client):
    mock_repo = MagicMock()
    mock_repo.get_user_by_email.return_value = {
        "id": 1,
        "role": "Student",
        "email": "test@example.com",
        "name": "Test User",
        "status": "active"
    }
    mock_repo_class.return_value = mock_repo

    mock_state = MagicMock()
    mock_state.google_login.return_value = (
        mock_repo.get_user_by_email.return_value,
        None
    )

    def fake_setup_session(user, session_obj):
        session_obj["email"] = user["email"]
        session_obj["id"] = user["id"]
        session_obj["role"] = user["role"]

    mock_state.setup_session.side_effect = fake_setup_session
    mock_get_state.return_value = mock_state

    response = client.post("/auth/google-login", json={"token": "fake-token"})

    assert response.status_code == 200
    assert response.json["message"] == "Login con Google exitoso"

@patch("app.controllers.auth.AuthStateContext.get_state")
def test_google_login_new_user(mock_get_state, client):
    mock_state = MagicMock()

    mock_state.google_login.return_value = ({
        "id": 2,
        "role": "Student",
        "email": "newuser@example.com",
        "name": "New User",
        "status": "pending"
    }, None)

    def fake_setup_session(user, session_obj):
        session_obj["email"] = user["email"]
        session_obj["id"] = user["id"]
        session_obj["role"] = user["role"]

    mock_state.setup_session.side_effect = fake_setup_session
    mock_get_state.return_value = mock_state

    response = client.post("/auth/google-login", json={"token": "fake-token"})

    assert response.status_code == 200
    assert response.json["message"] == "Login con Google exitoso"
