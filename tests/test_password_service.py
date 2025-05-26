from flask import redirect, url_for, flash, request
from app.models.services.email_service import EmailService
from app.models.builders.email_notification_builders import Builder
from app.models.services import email_service
from app.models.services import password_service
from app.models.services import email_notifier
from app.models.services.password_service import PasswordService


def test_validate_password():
    password_service_instance = PasswordService()

    #simbol missing
    password_test_1 = "Contraseña1234"
    is_valid = password_service_instance.validate_password(password_test_1)
    assert False == is_valid

    #password lenght less than 8
    password_test_2 = "Pass12*"
    is_valid = password_service_instance.validate_password(password_test_2)
    assert False == is_valid

    #Theres uppercase, lowercase, 8 characters and a simbol
    password_test_3 = "Pass123*"
    is_valid = password_service_instance.validate_password(password_test_3)
    assert True == is_valid

    #Uppercase letter missing
    password_test_4 = "password5751*"
    is_valid = password_service_instance.validate_password(password_test_4)
    assert False == is_valid

    #Number missing
    password_test_5 = "*.Passtraseña*+FxfAp"
    is_valid = password_service_instance.validate_password(password_test_5)
    assert False == is_valid

    #Lowercase missing
    password_test_6 = "PASSTRASEÑA54121*++"
    is_valid = password_service_instance.validate_password(password_test_6)
    assert False == is_valid


