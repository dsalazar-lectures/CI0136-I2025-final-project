# Bibliotecas para un manejo seguro de credenciales
import os
from dotenv import load_dotenv

# Bibliotecas para crear y enviar un mensaje por email
import smtplib
from email.message import EmailMessage

from app.services.notification.I_notification_type import NotificationService

# Clase que envía un correo electrónico
class SMTPEmailService(NotificationService):
  def __init__(self):
    # Leemos un .env donde se encuentran credenciales del correo que enviará el email
    load_dotenv()
    self.emailSender = os.getenv("SENDER")  # Obtenemos la dirección de correo electrónico
    self.passwordSender = os.getenv("PASSWORD")  # Obtenemos la contraseña

  def send(self, data):
    # Construcción del email
    email = EmailMessage()
    email["From"] = self.emailSender
    email["To"] = data["to"]
    email["Subject"] = data["subject"]
    email.set_content(data["message"])

    # Envío del email con smtp
    try:
      with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(self.emailSender, self.passwordSender)
        smtp.send_message(email)
      return True
    except Exception as e:
      print(f"Error: {e}")
      return False
