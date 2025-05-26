import pytest
from app import app as flask_app
from unittest.mock import MagicMock

@pytest.fixture(autouse=True)
def mock_db(monkeypatch):
    mock = MagicMock()
    # Patch db in all modules where it's imported at the top level
    monkeypatch.setattr("app.firebase_config.db", mock)
    monkeypatch.setattr("app.services.audit.file_audit_observer.db", mock, raising=False)
    monkeypatch.setattr("app.models.repositories.firebase_log_repository.db", mock, raising=False)
    monkeypatch.setattr("app.models.repositories.tutorial.firebase_tutorings_repository.db", mock, raising=False)
    # Add more if you import db elsewhere

# Set up the Flask app for testing (enables test mode)
@pytest.fixture
def app():
    flask_app.config["TESTING"] = True
    return flask_app

# Returns a test client to simulate requests without starting the server
@pytest.fixture
def client(app):
    return app.test_client()

# Auth helper to simplify login and registration in tests
@pytest.fixture
def auth(client):
    class AuthActions:
        # Logs in a user with the given email and password
        def login(self, email, password):
            return client.post("/login", data={
                "email": email,
                "password": password
            }, follow_redirects=True)

        # Registers a user with the provided name, email, password, and role
        def register(self, email, password, name, role):
            return client.post("/register", data={
                "name": name,
                "email": email,
                "password": password,
                "role": role
            }, follow_redirects=True)

    return AuthActions()