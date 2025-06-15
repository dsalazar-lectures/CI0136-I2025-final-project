# Biblioteca para la clase abstracta
from abc import ABC, abstractmethod

# Bibliotecas para un manejo seguro de credenciales
import os
from dotenv import load_dotenv

# Bibliotecas para crear y enviar un mensaje por email
import smtplib
from email.message import EmailMessage

# Clase abstracta para el servicio de notificaciones por correo electrnico
class EmailService(ABC):
  @abstractmethod
  def send_email(self, to: str, subject: str, message: str) -> bool:
    pass

# Clase que envía un correo electrónico
class SMTPEmailService(EmailService):
  def __init__(self):
    # Leemos un .env donde se encuentran credenciales del correo que enviará el email
    load_dotenv()
    self.emailSender = os.getenv("SENDER")  # Obtenemos la dirección de correo electrónico
    self.passwordSender = os.getenv("PASSWORD")  # Obtenemos la contraseña

  def send_email(self, to, subject, message):
    # Construcción del email
    email = EmailMessage()
    email["From"] = self.emailSender
    email["To"] = to
    email["Subject"] = subject
    email.set_content(message)

    # Envío del email con smtp
    try:
      with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(self.emailSender, self.passwordSender)
        smtp.send_message(email)
      return True
    except Exception as e:
      print(f"Error: {e}")
      return False

class Ban(SMTPEmailService):
  def __init__(self):
    super().__init__()
    self.subject = "Ban Notification"
    self.message = "Yoyu made a mistake so you are going to get a ban"
  
  def notify(self,to):
    return self.send_email(to,self.subject,self.message)