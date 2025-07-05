from .i_notification_builder import IBuilder
import datetime

class InscriptionStudenteEmailBuilder(IBuilder):
  """
  Class to build the email for student inscription.
  """

  always_notify = False

  def build_body(self, data):
    """
    Build the body of the email for student inscription.

    :param data: Dictionary containing the data for the email.
    Args:
      - username (str): The name of the user.
      - emailTo (str): The email address to send the notification to.
      - tutorial (str): The tutorial the user has signed up for.
    
    :return: Dictionary with the email details.
      - to (str): The email address to send the notification to.
      - subject (str): The subject of the email.
      - body (str): The body of the email containing the username, tutorial, and current date and time.
  
    :raises ValueError: If any required field is missing.
    """

    username = data.get("username")
    if username is None:
      raise ValueError("El nombre de usuario no puede ser nulo")
    
    email_to = data.get("emailTo")
    if email_to is None:
      raise ValueError("El correo electrónico no puede ser nulo")
    
    tutorial = data.get("tutorial")
    if tutorial is None:
      raise ValueError("El tutorial no puede ser nulo")

    return {
      "to": email_to,
      "subject": "Inscripción exitosa",
      "body": "Hola, " + username + ", usted se ha inscrito correctamente en la tutoria: " + tutorial + ".\n\n" + "Fecha y hora de inscripción: "
           + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

class InscriptionTutorEmailBuilder(IBuilder):
  """
  Class to build the email for tutor inscription.
  """
  always_notify = False

  def build_body(self, data):
    """
    Build the body of the email for student inscription.

    :param data: Dictionary containing the data for the email.
    Args:
      - studentname (str): The name of the student.
      - tutorname (str): The name of the tutor.
      - emailTo (str): The email address to send the notification to.
      - tutorial (str): The tutorial the user has signed up for.
    
    :return: Dictionary with the email details.
      - to (str): The email address to send the notification to.
      - subject (str): The subject of the email.
      - body (str): The body of the email containing the username, tutorial, and current date and time.
  
    :raises ValueError: If any required field is missing.
    """

    studentname = data.get("studentname")
    if studentname is None:
      raise ValueError("The student name can't be None")
    
    tutorname = data.get("tutorname")
    if tutorname is None:
      raise ValueError("The tutor name can't be None")
    
    email_to = data.get("emailTo")
    if email_to is None:
      raise ValueError("The email address can't be None")
    
    tutorial = data.get("tutorial")
    if tutorial is None:
      raise ValueError("Tutorial can't be None")

    return {
      "to": email_to,
      "subject": "¡Nueva inscripción!",
      "body": "Hola, " + tutorname +". El usuario" + studentname + ", ahora es estudiante en su tutoria: " + tutorial + ".\n\n" + "Fecha y hora de inscripción: "
           + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
