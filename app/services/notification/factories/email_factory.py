# Acceso al Ifactory
from app.services.notification.factories.I_builder_factories import BuilderFactory
# Acceso a los builders
from app.services.notification.builders.I_notification_builder import Builder
from app.services.notification.builders.I_notification_builder import email_notification_builders

# Clase fabrica para los builders de tipo email
class EmailBuilderFactory(BuilderFactory):
  def createBuilder(self, builderType: str) -> Builder:
    if builderType == "login":
      return email_notification_builders.loginEmailBuilder()
    elif builderType == "reminder":
      return email_notification_builders.ReminderEmailBuilder()
    else:
      raise ValueError("Builder no soportado")
