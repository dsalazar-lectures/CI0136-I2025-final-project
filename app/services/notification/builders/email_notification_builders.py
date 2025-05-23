from .i_notification_builder import IBuilder
import datetime

# Clase que estructura un correo de tipo login
class LoginEmailBuilder(IBuilder):
  """
  Clase LoginEmailBuilder
  Se encarga de construir el cuerpo del correo a la hora de iniciar sesión
  """
  def build_body(self, data: dict) -> dict:
    """
    Construye el cuerpo del correo de inicio de sesión.

    Args:
      data (dict): Diccionario con la información necesaria para el correo.
        - username (str): Nombre de usuario del destinatario.
        - emailTo (str): Correo electrónico del destinatario.

    Returns:
      dict: Diccionario con la información del correo a enviar.
        - to (str): Correo electrónico del destinatario.
        - subject (str): Asunto del correo electrónico.
        - body (str): Cuerpo del mensaje del correo.

    Raises:
      ValueError: Si el nombre de usuario o el correo electrónico son nulos.
    """
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
  """
  Clase ReminderEmailBuilder
  Se encarga de construir el cuerpo del correo de recordatorio de una tutoría.
  """
  def build_body(self, data: dict) -> dict:
    """
    Construye el cuerpo del correo de recordatorio.

    Args:
      data (dict): Diccionario con la información necesaria para el correo.
        - username (str): Nombre de usuario del destinatario.
        - emailTo (str): Correo electrónico del destinatario.
        - tutorial (str): Tutoría de la que se está haciendo un recordatorio.

    Returns:
      dict: Diccionario con la información del correo a enviar.
        - to (str): Correo electrónico del destinatario.
        - subject (str): Asunto del correo electrónico.
        - body (str): Cuerpo del mensaje del correo.

    Raises:
      ValueError: Si el nombre de usuario, correo electrónico o tutoria son nulos.
    """
    username = data.get("username")
    if username is None:
      raise ValueError("El usuario no puede ser nulo")
    email_to = data.get("emailTo")
    if email_to is None:
      raise ValueError("El correo electrónico no puede ser nulo")
    tutorial = data.get("tutoria")
    if tutorial is None:
      raise ValueError("La tutoría no puede ser nula")

    return {
      "to": email_to,
      "subject": "Recordatorio de tutoría",
      "body": "¡" + username + "!, recuerde que su tutoría de " + tutorial + ", inicia en 1 hora"
    }
