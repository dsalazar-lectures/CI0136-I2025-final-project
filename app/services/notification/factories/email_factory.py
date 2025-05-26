# Acceso al Ifactory
from .i_builder_factories import IBuilderFactory
# Acceso a los builders
from ..builders import *

# Clase fabrica para los builders de tipo email
class EmailBuilderFactory(IBuilderFactory):
  def create_builder(self, builder_type: str) -> IBuilder:
    if builder_type == "login":
      return email_notification_builders.LoginEmailBuilder()
    elif builder_type == "reminder":
      return email_notification_builders.ReminderEmailBuilder()
    elif builder_type == "recoveryPassword":
      return email_notification_builders.PasswordRecoveryEmailBuilder()
    elif builder_type == "successPasswordChange":
      return email_notification_builders.SuccessPasswordChangeEmailBuilder()
    elif builder_type == "successRegister":
      return email_notification_builders.SuccessRegisterEmailBuilder()
    elif builder_type == "newTutorial":
      return email_notification_builders.NewTutorialEmailBuilder()
    else:
      raise ValueError("Builder no soportado")
