# Bibliotecas para crear y enviar un mensaje por email
import smtplib
from email.message import EmailMessage

from .i_notification_type import INotificationService

# Clase que envía un correo electrónico usando smtp
class SMTPEmailService(INotificationService):
  """
  Servicio de envío de correos electrónicos utilizando el servidor SMTP de Gmail.

  Atributos:
    emailSender (str): Dirección de correo del remitente.
    passwordSender (str): Contraseña o clave de aplicación del remitente.
  """

  def __init__(self, emailSender: str, passwordSender: str):
    self.emailSender = emailSender  # Obtenemos el email
    self.passwordSender = passwordSender  # Obtenemos la contraseña

  def send(self, data) -> bool:
    """
    Envía un correo electrónico utilizando el servidor SMTP de Gmail.

    Parámetros:
    ----------
    data : dict
      Diccionario que contiene la información del correo electrónico:
      - 'to': Correo electrónico del destinatario.
      - 'subject': Asunto del correo electrónico.
      - 'message': Cuerpo del mensaje del correo electrónico.

    Retorna:
    -------
    bool
      - True si el correo electrónico se envió correctamente.
      - False en caso contrario.
    """
    # Construcción del email
    email = EmailMessage()
    email["From"] = self.emailSender
    email["To"] = data["to"]
    email["Subject"] = data["subject"]
    email.set_content(data["body"])

    # Envío del email con smtp
    try:
      with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(self.emailSender, self.passwordSender)
        smtp.send_message(email)
      return True
    except Exception as e:
      print(f"Error: {e}")
      return False
