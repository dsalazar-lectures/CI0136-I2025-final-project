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

# Clase que estructura un correo de recuperación de contraseña
class PasswordRecoveryEmailBuilder(IBuilder):
  """
  Clase PasswordRecoveryEmailBuilder
  Se encarga de construir el cuerpo del correo de recuperación de contraseña.
  """
  def build_body(self, data: dict) -> dict:
    """
    Construye el cuerpo del correo de recuperación de contraseña.

    Args:
      data (dict): Diccionario con la información necesaria para el correo.
        - username (str): Nombre de usuario del destinatario.
        - emailTo (str): Correo electrónico del destinatario.
        - reset_link (str): Enlace para restablecer la contraseña.

    Returns:
      dict: Diccionario con la información del correo a enviar.
        - to (str): Correo electrónico del destinatario.
        - subject (str): Asunto del correo electrónico.
        - body (str): Cuerpo del mensaje del correo.

    Raises:
      ValueError: Si el nombre de usuario, correo electrónico o enlace de restablecimiento son nulos.
    """
    username = data.get("username")
    if username is None:
      raise ValueError("El nombre de usuario no puede ser nulo")
    
    email_to = data.get("emailTo")
    if email_to is None:
      raise ValueError("El correo electrónico no puede ser nulo")
    
    reset_link = data.get("reset_link")
    if reset_link is None:
      raise ValueError("El enlace de restablecimiento no puede ser nulo")

    return {
      "to": email_to,
      "subject": "Recuperación de contraseña",
      "body": "Hola " + username + ", hemos recibido una solicitud para restablecer su contraseña "
      + "a las " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
      + "Haga clic en el siguiente enlace para restablecer su contraseña: " + reset_link + "\n"
      + "Este enlace es válido por 15 minutos.\n\n" 
      + "Si no solicitó este cambio, ignore este correo.\n"
    }
  
class SuccessPasswordChangeEmailBuilder(IBuilder):
  """
  Clase SuccessPasswordChangeEmailBuilder
  Se encarga de construir el cuerpo del correo de cambio de contraseña exitoso.
  """
  def build_body(self, data: dict) -> dict:
    """
    Construye el cuerpo del correo de cambio de contraseña exitoso.

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
      "subject": "Cambio de contraseña exitoso",
      "body": "Hola " + username + ", su contraseña ha sido cambiada exitosamente!\n"
          + "Su contraseña se modificó a las " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
          + "Si usted no realizó ese cambio, por favor comuníquese con soporte al cliente, soporteFlask@gmail.com.\n"
          + "Gracias por usar nuestro servicio.\n"
    }
