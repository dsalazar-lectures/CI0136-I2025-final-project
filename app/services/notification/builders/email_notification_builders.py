from app.services.notification.builders.I_notification_builder import Builder

import datetime

# Clase que estructura un correo de tipo login
class loginEmailBuilder(Builder):
  def buildBody(self, data: dict) -> dict:
    username = data.get("username")
    if username is None:
      raise ValueError("El nombre de usuario no puede ser nulo")
    
    emailTo = data.get("emailTo")
    if emailTo is None:
      raise ValueError("El correo electrónico no puede ser nulo")

    return {
        "to": emailTo,
        "subject": "Inicio de sesión exitoso",
        "body": "Bienvenido de nuevo " + username + ", ha iniciado sesión exitosamente "
                + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# Clase que estructura un correo de tipo reminder
class ReminderEmailBuilder(Builder):
  def buildBody(self, data: dict) -> dict:
    username = data.get("username")
    if username is None:
      raise ValueError("El usuario no puede ser nulo")
    emailTo = data.get("emailTo")
    if emailTo is None:
      raise ValueError("El correo electrónico no puede ser nulo")
    tutoria = data.get("tutoria")
    if tutoria is None:
      raise ValueError("La tutoría no puede ser nula")

    return {
        "to": emailTo,
        "subject": "Recordatorio de tutoría",
        "body": "¡" + username + "!, recuerde que su tutoría de " + tutoria + ", inicia en 1 hora"
    }
