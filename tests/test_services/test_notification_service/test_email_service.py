import pytest
from unittest import mock

from app.services.notification import EmailService
from app.services.notification import EmailBuilderFactory
from app.services.notification import SMTPEmailService


# test para validar que el servicio de email se crea correctamente
def test_create_email_service():
    factory = EmailBuilderFactory()
    smtp_service = SMTPEmailService("smtp.example.com", "password")
    email_service = EmailService(factory, smtp_service)
    assert email_service is not None
    assert isinstance(email_service, EmailService)

# test para validar que el email se envía correctamente con  los parámetros correctos
def test_send_email_correct():
    factory = EmailBuilderFactory()
    # Mock the SMTP service
    smtp_service = mock.Mock(spec=SMTPEmailService)
    smtp_service.send.return_value = True
    email_service = EmailService(factory, smtp_service)
    result = email_service.send_email('login', {'username':'JJ','emailTo': '123@123.com'})
    assert result is True

# test para validar que el email no se envía si el builder no existe
def test_send_email_incorrect_build_parameter():
    factory = EmailBuilderFactory()
    # Mock the SMTP service
    smtp_service = mock.Mock(spec=SMTPEmailService)
    smtp_service.send.return_value = True
    email_service = EmailService(factory, smtp_service)
    result = email_service.send_email('abc', {'username':'JJ','emailTo': '123@123.com'})
    assert result is False

# test para validar que el email no se envia si el diccionario no es correcto
def test_send_email_incorrect_data_parameter():
    factory = EmailBuilderFactory()
    # Mock the SMTP service
    smtp_service = mock.Mock(spec=SMTPEmailService)
    smtp_service.send.return_value = True
    email_service = EmailService(factory, smtp_service)
    result = email_service.send_email('login', {'usernam':'JJ','emailTo': '123@123.com'})
    assert result is False

# test para validar que el servicio de email no funciona no se envía el correo
def test_send_email_incorrect_smtp():
    factory = EmailBuilderFactory()
    # Mock the SMTP service
    smtp_service = mock.Mock(spec=SMTPEmailService)
    smtp_service.send.return_value = False
    email_service = EmailService(factory, smtp_service)
    result = email_service.send_email('login', {'username':'JJ','emailTo': '123@123.com'})
    assert result is False
                                                


