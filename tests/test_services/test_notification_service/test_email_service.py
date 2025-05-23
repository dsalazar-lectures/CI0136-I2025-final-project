import pytest

from app.services.notification import Emailservice

@pytest.fixture
def email_service():
    return Emailservice()


def test_create_email_service(email_service):
    assert email_service is not None
    assert isinstance(email_service, Emailservice)

    