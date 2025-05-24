import pytest
from app.models.services.registration_service import validate_registration_data
from app.models.repositories.users.firebase_user_repository import FirebaseUserRepository

# Test that valid roles are accepted without triggering validation errors
@pytest.mark.parametrize("valid_role", ["Student", "Administrator", "Tutor"])
def test_valid_roles_are_accepted(valid_role):
    user_repo = FirebaseUserRepository()
    data = {
        "email": "test@example.com",
        "password": "ValidPass123!",
        "role": valid_role,
        "name": "Test User"
    }

    # Call the validation function with a valid role
    error_message, category = validate_registration_data(
        name=data["name"],
        email=data["email"],
        password=data["password"],
        role=data["role"],
        user_repo=user_repo
    )

    # Should not return any error for valid roles
    assert error_message is None, f"Expected role '{valid_role}' to be valid"

# Test that invalid roles are properly rejected and trigger validation errors
@pytest.mark.parametrize("invalid_role", ["Admin", "Guest", "SuperUser", "", "student", "tutor"])
def test_invalid_roles_are_rejected(invalid_role):
    user_repo = FirebaseUserRepository()
    data = {
        "email": "test2@example.com",
        "password": "ValidPass123!",
        "role": invalid_role,
        "name": "Test User"
    }

    # Call the validation function with an invalid role
    error_message, category = validate_registration_data(
        name=data["name"],
        email=data["email"],
        password=data["password"],
        role=data["role"],
        user_repo=user_repo
    )

    # Expect an error message indicating the role is not allowed
    assert error_message is not None, f"Expected role '{invalid_role}' to be rejected"
    assert isinstance(error_message, str), "Expected an error message string"
