"""
__init__.py
En este archivo se importan las clases que se encuentran en el directorio.
"""

from .email_service import *
from .builders import *
from .factories import *
from .types import *



from os import environ

# Creamos una instancia del servicio de correo electrónico
factory = EmailBuilderFactory()

email_sender = environ.get("SENDER", "")
password = environ.get("PASSWORD", "")

smtp_service = SMTPEmailService(emailSender=email_sender, passwordSender=password)

email_service = EmailService(factory, smtp_service)
 

def send_email_notification(email_type: str, data: dict) -> bool:
    """
    Envia una notificación por correo electrónico.

    Parámetros:
        email_type (str): Tipo de notificación que se quiere enviar (Login, Reminder, etc).
        data (dict): Diccionario que contiene los datos necesarios para crear el cuerpo de la notificación.
    Retorna:
        bool: True si el correo se envió correctamente, False en caso contrario.
    """
    return email_service.send_email(email_type, data)
