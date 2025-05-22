from app.services.notification.builders.I_notification_builder import Builder


# Clase que estructura un correo de tipo login
class loginEmailBuilder(Builder):
  def buildBody(self):
    return {
        "subject": "Inicio de sesión exitoso",
        "body": "Bienvenido de nuevo (Usuario), ha iniciado sesión exitosamente a las (time)"
    }

# Clase que estructura un correo de tipo reminder
class ReminderEmailBuilder(Builder):
  def buildBody(self):
    return {
        "subject": "Recordatorio de tutoría",
        "body": "¡(user.name)!, recuerde que su tutoría de (tutoría), inicia en 1 hora"
    }
