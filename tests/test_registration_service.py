"""
Tests for user registration and login validation services.
"""
import pytest
from app.models.repositories.users.mock_user_repository import MockUserRepository
from app.models.services.registration_service import validate_registration_data, validate_login_data
import bcrypt

@pytest.fixture
def mock_repo():
    """Returns a mock user repository for testing."""
    return MockUserRepository()

def test_validate_registration_data_success(mock_repo):
    error_message, category = validate_registration_data(
        name="Test User",
        email="newuser@example.com",
        password="Password1@",
        role="Student",
        user_repo=mock_repo
    )
    assert error_message is None
    assert category is None

def test_validate_registration_missing_fields(mock_repo):
    error_message, category = validate_registration_data(
        name="",
        email="",
        password="",
        role="Student",
        user_repo=mock_repo
    )
    assert error_message == 'All fields are required.'
    assert category == 'danger'

def test_validate_registration_invalid_email(mock_repo):
    error_message, category = validate_registration_data(
        name="Test User",
        email="invalidemail",
        password="Password1@",
        role="Student",
        user_repo=mock_repo
    )
    assert error_message == 'Invalid email.'
    assert category == 'danger'

def test_validate_registration_weak_password(mock_repo):
    error_message, category = validate_registration_data(
        name="Test User",
        email="test@example.com",
        password="weak",
        role="Student",
        user_repo=mock_repo
    )
    assert error_message == 'Password must include at least one uppercase letter, one number, and one special character.'
    assert category == 'danger'

def test_validate_login_success(mock_repo):
    """Tests successful login validation with valid credentials."""
    user, error = validate_login_data(
        email="admin@example.com",
        password="Admin1@",
        user_repo=mock_repo
    )
    assert user is not None
    assert error is None

def test_validate_login_invalid_credentials(mock_repo):
    """Tests login validation with invalid credentials."""
    user, error = validate_login_data(
        email="wrong@example.com",
        password="wrongpass",
        user_repo=mock_repo
    )
    assert user is None
    assert error == "Invalid credentials."


class MockUserRepository:
    def __init__(self):
        self.users = [
            {
                "email": "admin@example.com",
                "password": bcrypt.hashpw("Admin1@".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                "role": "Administrator"
            }
        ]
    def get_user_by_email(self, email):
        for user in self.users:
            if user["email"] == email:
                return user
        return None