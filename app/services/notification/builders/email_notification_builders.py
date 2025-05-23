from .i_notification_builder import IBuilder
import datetime

# Clase que estructura un correo de tipo login
class LoginEmailBuilder(IBuilder):
  def build_body(self, data: dict) -> dict:
    username = data.get("username")
    if username is None:
      raise ValueError("El nombre de usuario no puede ser nulo")
    
    email_to = data.get("emailTo")
    if email_to is None:
      raise ValueError("El correo electrónico no puede ser nulo")

    return {
        "to": email_to,
        "subject": "Inicio de sesión exitoso",
        "body": "Bienvenido de nuevo " + username + ", ha iniciado sesión exitosamente "
                + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# Clase que estructura un correo de tipo reminder
class ReminderEmailBuilder(IBuilder):
  def build_body(self, data: dict) -> dict:
    username = data.get("username")
    if username is None:
      raise ValueError("El usuario no puede ser nulo")
    email_to = data.get("emailTo")
    if email_to is None:
      raise ValueError("El correo electrónico no puede ser nulo")
    tutoria = data.get("tutoria")
    if tutoria is None:
      raise ValueError("La tutoría no puede ser nula")

    return {
        "to": email_to,
        "subject": "Recordatorio de tutoría",
        "body": "¡" + username + "!, recuerde que su tutoría de " + tutoria + ", inicia en 1 hora"
    }
