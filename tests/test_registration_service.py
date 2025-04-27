import pytest
from app.models.repositories.mock_user_repository import MockUserRepository
from app.models.services.registration_service import validate_registration_data, validate_login_data

@pytest.fixture
def mock_repo():
    return MockUserRepository()

def test_validate_registration_data_success(mock_repo):
    error_message, category = validate_registration_data(
        email="newuser@example.com",
        password="Password1@",
        role="Student",
        user_repo=mock_repo
    )
    assert error_message is None
    assert category is None

def test_validate_registration_missing_fields(mock_repo):
    error_message, category = validate_registration_data(
        email="",
        password="",
        role="Student",
        user_repo=mock_repo
    )
    assert error_message == 'All fields are required.'
    assert category == 'danger'

def test_validate_registration_invalid_email(mock_repo):
    error_message, category = validate_registration_data(
        email="invalidemail",
        password="Password1@",
        role="Student",
        user_repo=mock_repo
    )
    assert error_message == 'Invalid email.'
    assert category == 'danger'

def test_validate_registration_weak_password(mock_repo):
    error_message, category = validate_registration_data(
        email="test@example.com",
        password="weak",
        role="Student",
        user_repo=mock_repo
    )
    assert error_message == 'Password must include at least one uppercase letter, one number, and one special character.'
    assert category == 'danger'

def test_validate_login_success(mock_repo):
    user, error = validate_login_data(
        email="admin@example.com",
        password="Admin1@",
        user_repo=mock_repo
    )
    assert user is not None
    assert error is None

def test_validate_login_invalid_credentials(mock_repo):
    user, error = validate_login_data(
        email="wrong@example.com",
        password="wrongpass",
        user_repo=mock_repo
    )
    assert user is None
    assert error == "Invalid credentials."
