import pytest
from app import app as flask_app

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
