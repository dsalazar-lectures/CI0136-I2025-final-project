# Biblioteca para la clase abstracta
from abc import ABC, abstractmethod

# Acceso a los builders
from app.models.builders import email_notification_builders

# Clase abstracta para las fabricas
class BodyFactory(ABC):
  @abstractmethod
  def createBody(self, builderType: str, datos) -> email_notification_builders.Builder:
    pass

# Clase fabrica para los builders de tipo email
class EmailBuilderFactory(BodyFactory):
  def createBody(self, builderType: str) -> email_notification_builders.Builder:
    if builderType == "login":
      return email_notification_builders.loginEmailBuilder()
    elif builderType == "reminder":
      return email_notification_builders.ReminderEmailBuilder()
    elif builderType == "changepassword":
      return email_notification_builders.ChangePasswordEmailBuilder();
    else:
      raise ValueError("Builder no soportado")
