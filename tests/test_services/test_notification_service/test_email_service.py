import pytest

from app.services.notification import EmailService
from app.services.notification import EmailBuilderFactory
from app.services.notification import SMTPEmailService



def test_create_email_service():
    factory = EmailBuilderFactory()
    smtp_service = SMTPEmailService()
    email_service = EmailService(factory, smtp_service)
    assert email_service is not None
    assert isinstance(email_service, EmailService)

def test_send_email_correct(email_service):
    result = email_service.send_email('login', {'username':'JJ','emailTo': '123@123.com'})
    assert result is True


