# Acceso al Ifactory
from .i_builder_factories import BuilderFactory
# Acceso a los builders
from builders import *

# Clase fabrica para los builders de tipo email
class EmailBuilderFactory(BuilderFactory):
  def create_builder(self, builder_type: str) -> Builder:
    if builder_type == "login":
      return email_notification_builders.LoginEmailBuilder()
    elif builder_type == "reminder":
      return email_notification_builders.ReminderEmailBuilder()
    else:
      raise ValueError("Builder no soportado")
