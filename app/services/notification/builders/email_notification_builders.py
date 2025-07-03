from .i_notification_builder import IBuilder
import datetime

# Clase que estructura un correo de tipo login
class LoginEmailBuilder(IBuilder):
  always_notify = False
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
  
  def get_bypass_priority(self):
    return self.always_notify

# Clase que estructura un correo de tipo reminder
class ReminderEmailBuilder(IBuilder):
  always_notify = False
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
  
  def get_bypass_priority(self):
      return self.always_notify

# Clase que estructura un correo de recuperación de contraseña
class PasswordRecoveryEmailBuilder(IBuilder):
  always_notify = True
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
  
  def get_bypass_priority(self):
      return self.always_notify
  
class SuccessPasswordChangeEmailBuilder(IBuilder):
  always_notify = False
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
  
  def get_bypass_priority(self):
      return self.always_notify

class SuccessRegisterEmailBuilder(IBuilder):
  always_notify = False
  """
  Clase SuccessRegisterEmailBuilder
  Se encarga de construir el cuerpo del correo de registro exitoso.
  """
  def build_body(self, data: dict) -> dict:
    """
    Construye el cuerpo del correo de registro exitoso.

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
      "subject": "Registro exitoso",
      "body": "Hola " + username + ", su registro ha sido exitoso!\n"
          + "Su cuenta fue creada a las " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
          + "Gracias por usar nuestro servicio.\n"
    }
  
  def get_bypass_priority(self):
      return self.always_notify
  

class NewTutorialEmailBuilder(IBuilder):
  always_notify = False
  """
  Clase NewTutorialEmailBuilder
  Se encarga de construir el cuerpo del correo de nueva tutoría.
  """
  def build_body(self, data: dict) -> dict:
    """
    Construye el cuerpo del correo de nueva tutoría.

    Args:
      data (dict): Diccionario con la información necesaria para el correo.
        - username (str): Nombre de usuario del destinatario.
        - emailTo (str): Correo electrónico del destinatario.
        - tutorial (str): Tutoría que se ha creado.

    Returns:
      dict: Diccionario con la información del correo a enviar.
        - to (str): Correo electrónico del destinatario.
        - subject (str): Asunto del correo electrónico.
        - body (str): Cuerpo del mensaje del correo.

    Raises:
      ValueError: Si el nombre de usuario, correo electrónico o tutoría son nulos.
    """
    username = data.get("username")
    if username is None:
      raise ValueError("El nombre de usuario no puede ser nulo")
    
    email_to = data.get("emailTo")
    if email_to is None:
      raise ValueError("El correo electrónico no puede ser nulo")
    
    tutorial = data.get("tutorial")
    if tutorial is None:
      raise ValueError("La tutoría no puede ser nula")

    return {
      "to": email_to,
      "subject": "Nueva tutoría",
      "body": "Hola " + username + ", se ha creado una nueva tutoría: " + tutorial + "\n"
          + "Gracias por usar nuestro servicio.\n"
    }
  
  def get_bypass_priority(self):
      return self.always_notify

class TutorialCancelledEmailBuilder(IBuilder):
  always_notify = False
  """
  Clase TutorialCancelledEmailBuilder
  Se encarga de construir el cuerpo del correo de cancelación de tutoría.
  """
  def build_body(self, data: dict) -> dict:
    """
    Construye el cuerpo del correo de cancelación de tutoría.

    Args:
      data (dict): Diccionario con la información necesaria para el correo.
        - username (str): Nombre de usuario del destinatario.
        - emailTo (str): Correo electrónico del destinatario.
        - tutorial (str): Tutoría que ha sido cancelada.

    Returns:
      dict: Diccionario con la información del correo a enviar.
        - to (str): Correo electrónico del destinatario.
        - subject (str): Asunto del correo electrónico.
        - body (str): Cuerpo del mensaje del correo.

    Raises:
      ValueError: Si el nombre de usuario, correo electrónico o tutoría son nulos.
    """
    username = data.get("username")
    if username is None:
      raise ValueError("El nombre de usuario no puede ser nulo")
    
    email_to = data.get("emailTo")
    if email_to is None:
      raise ValueError("El correo electrónico no puede ser nulo")
    
    tutorial = data.get("tutorial")
    if tutorial is None:
      raise ValueError("La tutoría no puede ser nula")

    return {
      "to": email_to,
      "subject": "Tutoría Cancelada",
      "body": f"Hola {username},\n\n"
          + f"La tutoría '{tutorial}' ha sido cancelada.\n"
          + "Te sugerimos revisar otras tutorías disponibles en el sistema.\n\n"
          + "Gracias por tu comprensión.\n"
    }
  
  def get_bypass_priority(self):
      return self.always_notify

class NewCommentEmailBuilder(IBuilder):
  always_notify = True
  """
  Clase NewCommentEmailBuilder
  Se encarga de construir el cuerpo del correo cuando se recibe un comentario/reseña nueva
  """
  def build_body(self, data: dict) -> dict:
    """
    Construye el cuerpo del correo de nuevo comentario.

    Args:
      data (dict): Diccionario con la información necesaria para el correo.
        - username (str): Nombre de usuario del destinatario (tutor).
        - emailTo (str): Correo electrónico del destinatario.
        - student_name (str): Nombre del estudiante que comentó.
        - comment (str): Texto del comentario.
        - rating (int): Calificación de estrellas.
        - tutorial (str): Nombre de la tutoría.

    Returns:
      dict: Diccionario con la información del correo a enviar.
        - to (str): Correo electrónico del destinatario.
        - subject (str): Asunto del correo electrónico.
        - body (str): Cuerpo del mensaje del correo.

    Raises:
      ValueError: Si los datos requeridos son nulos.
    """
    username = data.get("username")
    if username is None:
      raise ValueError("El nombre de usuario no puede ser nulo")
    
    email_to = data.get("emailTo")
    if email_to is None:
      raise ValueError("El correo electrónico no puede ser nulo")
    
    student_name = data.get("student_name")
    if student_name is None:
      raise ValueError("El nombre del estudiante no puede ser nulo")
    
    comment = data.get("comment", "")
    rating = data.get("rating", 0)
    tutorial = data.get("tutorial", "")

    stars = "⭐" * int(rating) if rating > 0 else ""

    return {
      "to": email_to,
      "subject": f"Nuevo comentario en tu tutoría: {tutorial}",
      "body": f"Hola {username},\n\n"
          + f"Has recibido un nuevo comentario en tu tutoría '{tutorial}'.\n\n"
          + f"Comentario de: {student_name}\n"
          + f"Calificación: {stars} ({rating}/5)\n"
          + f"Mensaje: {comment}\n\n"
          + "Puedes responder al comentario desde la plataforma.\n\n"
    }
  
  def get_bypass_priority(self):
    return self.always_notify

class TutorReplyEmailBuilder(IBuilder):
  always_notify = True
  """
  Clase TutorReplyEmailBuilder
  Se encarga de construir el cuerpo del correo cuando un tutor responde a un comentario
  """
  def build_body(self, data: dict) -> dict:
    """
    Construye el cuerpo del correo de respuesta de tutor.

    Args:
      data (dict): Diccionario con la información necesaria para el correo.
        - username (str): Nombre de usuario del destinatario (estudiante).
        - emailTo (str): Correo electrónico del destinatario.
        - tutor_name (str): Nombre del tutor que respondió.
        - reply (str): Texto de la respuesta.
        - tutorial (str): Nombre de la tutoría.
        - original_comment (str): Comentario original del estudiante.

    Returns:
      dict: Diccionario con la información del correo a enviar.
        - to (str): Correo electrónico del destinatario.
        - subject (str): Asunto del correo electrónico.
        - body (str): Cuerpo del mensaje del correo.

    Raises:
      ValueError: Si los datos requeridos son nulos.
    """
    username = data.get("username")
    if username is None:
      raise ValueError("El nombre de usuario no puede ser nulo")
    
    email_to = data.get("emailTo")
    if email_to is None:
      raise ValueError("El correo electrónico no puede ser nulo")
    
    tutor_name = data.get("tutor_name")
    if tutor_name is None:
      raise ValueError("El nombre del tutor no puede ser nulo")
    
    reply = data.get("reply", "")
    tutorial = data.get("tutorial", "")
    original_comment = data.get("original_comment", "")

    return {
      "to": email_to,
      "subject": f"Respuesta del tutor en: {tutorial}",
      "body": f"Hola {username},\n\n"
          + f"El tutor {tutor_name} ha respondido a tu comentario en la tutoría '{tutorial}'.\n\n"
          + f"Tu comentario original:\n"
          + f"'{original_comment}'\n\n"
          + f"Respuesta del tutor:\n"
          + f"'{reply}'\n\n"
          + "Puedes ver la conversación completa en la plataforma.\n\n"
    }
  
  def get_bypass_priority(self):
    return self.always_notify