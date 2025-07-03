import pytest
from unittest.mock import MagicMock

@pytest.fixture(scope="module")
def email_service_mock():
    mock = MagicMock()
    mock.send_email = MagicMock(return_value=True)
    return mock

@pytest.fixture(scope="module")
def valid_test_email():
    return "test@example.com"

@pytest.fixture(scope="module")
def invalid_test_emails():
    return ["", None, "invalid-email", "@no-user.com"]
