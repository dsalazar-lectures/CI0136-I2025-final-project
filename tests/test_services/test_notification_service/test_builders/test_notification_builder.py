import pytest
from app.services.notification.builders import LoginEmailBuilder
from app.services.notification.builders import ReminderEmailBuilder
from app.services.notification.builders import IBuilder
import datetime
from unittest.mock import patch


def test_login_email_builder():
    builder = LoginEmailBuilder()
    assert builder is not None
    assert isinstance(builder, IBuilder)

    data = {
        "username": "test_user",
        "emailTo": "123@123.com",
    }

    fake_now = datetime.datetime(2023, 10, 1, 12, 0, 0)

    with patch("datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value = fake_now
        mock_datetime.strftime = datetime.datetime.strftime
        result = builder.build_body(data)

    expected_body = (
        "Bienvenido de nuevo test_user, ha iniciado sesión exitosamente 2023-10-01 12:00:00"
    )

    assert result["to"] == "123@123.com"
    assert result["subject"] == "Inicio de sesión exitoso"
    assert result["body"] == expected_body

def test_login_email_builder_missing_username():
    builder = LoginEmailBuilder()
    data = {
        "emailTo": "123@123.com"
    }
    with pytest.raises(ValueError) as excinfo:
        builder.build_body(data)
    assert str(excinfo.value) == "El nombre de usuario no puede ser nulo"

def test_login_email_builder_missing_email():
    builder = LoginEmailBuilder()
    data = {
        "username": "test_user"
    }
    with pytest.raises(ValueError) as excinfo:
        builder.build_body(data)
    assert str(excinfo.value) == "El correo electrónico no puede ser nulo"

def test_login_email_builder_missing_data():
    builder = LoginEmailBuilder()
    data = {}
    with pytest.raises(ValueError) as excinfo:
        builder.build_body(data)
    assert str(excinfo.value) == "El nombre de usuario no puede ser nulo"


def test_reminder_email_builder():
    builder = ReminderEmailBuilder()
    assert builder is not None
    assert isinstance(builder, IBuilder)

    data = {
        "username": "test_user",
        "emailTo": "123@123.com",
        "tutoria": "test_tutorial",
    }

    except_data = {
        "to": "123@123.com",
        "subject": "Recordatorio de tutoría",
        "body": "¡test_user!, recuerde que su tutoría de test_tutorial, inicia en 1 hora"
    }
    result = builder.build_body(data)
    assert result["to"] == except_data["to"]
    assert result["subject"] == except_data["subject"]
    assert result["body"] == except_data["body"]

def test_reminder_email_builder_missing_username():
    builder = ReminderEmailBuilder()
    data = {
        "emailTo": "123@123.com",
        "tutoria": "test_tutorial",
    }
    with pytest.raises(ValueError) as excinfo:
        builder.build_body(data)
    assert str(excinfo.value) == "El usuario no puede ser nulo"
def test_reminder_email_builder_missing_email():
    builder = ReminderEmailBuilder()
    data = {
        "username": "test_user",
        "tutoria": "test_tutorial",
    }
    with pytest.raises(ValueError) as excinfo:
        builder.build_body(data)
    assert str(excinfo.value) == "El correo electrónico no puede ser nulo"
def test_reminder_email_builder_missing_tutoria():
    builder = ReminderEmailBuilder()
    data = {
        "username": "test_user",
        "emailTo": "123@123.com",
    }
    with pytest.raises(ValueError) as excinfo:
        builder.build_body(data)
    assert str(excinfo.value) == "La tutoría no puede ser nula"

def test_reminder_email_builder_missing_data():
    builder = ReminderEmailBuilder()
    data = {}
    with pytest.raises(ValueError) as excinfo:
        builder.build_body(data)
    assert str(excinfo.value) == "El usuario no puede ser nulo"








