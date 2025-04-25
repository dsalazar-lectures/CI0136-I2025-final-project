from flask import Flask
from flask_mail import Message
from app.extensions import mail
import os
import dotenv
dotenv.load_dotenv()


def send_login_notification(recipient_email):
    msg = Message(
        subject='Notificación de inicio de sesión',
        sender=os.getenv('DEL_EMAIL'),
        recipients=[recipient_email]
    )
    msg.body = "Este es un correo de prueba enviado desde Flask."
    #mail.send(msg)