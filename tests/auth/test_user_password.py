import pytest
from app.models.services.registration_service import validate_registration_data
from app.models.repositories.users.firebase_user_repository import FirebaseUserRepository

# Test that various invalid password formats are correctly rejected
@pytest.mark.parametrize("invalid_password", [
    "short",
    "nouppercase1!",
    "NoSpecialChar1", 
    "NoNumber!",
    "12345678!",
])
def test_invalid_passwords_are_rejected(invalid_password):
    user_repo = FirebaseUserRepository()
    data = {
        "name": "Test User",
        "email": "passwordtest@example.com",
        "password": invalid_password,
        "role": "Student"
    }

    # Call the validation function with the invalid password
    error_message, category = validate_registration_data(
        name=data["name"],
        email=data["email"],
        password=data["password"],
        role=data["role"],
        user_repo=user_repo
    )

    # Make sure the password gets rejected and the error message mentions it
    assert error_message is not None, f"Expected password '{invalid_password}' to be rejected"
    assert "password" in error_message.lower(), f"Expected error message to mention password: {error_message}"


# Test that a valid password passes all validation rules
def test_valid_password_is_accepted():
    user_repo = FirebaseUserRepository()
    
    # This password has uppercase, lowercase, number, special character, and proper length
    error_message, category = validate_registration_data(
        name="Valid User",
        email="valid@example.com",
        password="ValidPass1!",
        role="Student",
        user_repo=user_repo
    )

    # Expect no error with a valid password
    assert error_message is None, "Expected a valid password to be accepted"
