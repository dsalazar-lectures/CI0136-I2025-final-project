# Acceso al Ifactory
from .i_builder_factories import BuilderFactory
# Acceso a los builders
from builders import *

# Clase fabrica para los builders de tipo email
class EmailBuilderFactory(BuilderFactory):
  def createBuilder(self, builderType: str) -> Builder:
    if builderType == "login":
      return email_notification_builders.loginEmailBuilder()
    elif builderType == "reminder":
      return email_notification_builders.ReminderEmailBuilder()
    else:
      raise ValueError("Builder no soportado")
