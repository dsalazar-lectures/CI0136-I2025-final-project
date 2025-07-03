import pytest
from app.models.services.registration_service import validate_registration_data
from app.models.repositories.users.firebase_user_repository import FirebaseUserRepository

# Tests that invalid email formats are correctly rejected by the validation logic
@pytest.mark.parametrize("invalid_email", [
    "",
    "plainaddress",
    "missingdomain@",
    "@missinguser.com",
    "user@.com",
    "user@com",
])
def test_invalid_emails_are_rejected(invalid_email):
    user_repo = FirebaseUserRepository()

    # Attempt to validate a user with an invalid email
    error_message, category = validate_registration_data(
        name="Rolandito",
        email=invalid_email,
        password="ValidPass1!",
        role="Student",
        user_repo=user_repo
    )

    # Expect an error and meaningful message
    assert error_message is not None
    assert (
        "email" in error_message.lower()
        or "invalid" in error_message.lower()
        or "required" in error_message.lower()
    )


# Tests that valid email formats pass validation without errors
@pytest.mark.parametrize("valid_email", [
    "user@example.com",
    "user.name@domain.co",
    "user_name@sub.domain.org",
    "user+alias@domain.io"
])
def test_valid_emails_are_accepted(valid_email):
    user_repo = FirebaseUserRepository()

    # Attempt to validate a user with a valid email
    error_message, category = validate_registration_data(
        name="Rolandito",
        email=valid_email,
        password="ValidPass1!",
        role="Student",
        user_repo=user_repo
    )

    # Expect no error for valid emails
    assert error_message is None
