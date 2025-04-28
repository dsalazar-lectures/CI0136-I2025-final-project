# Biblioteca para la clase abstracta
from abc import ABC, abstractmethod

# Clase abstracta para las notificaciones de tipo email
class Builder(ABC):
  @abstractmethod
  def buildBody(self) -> dict:
    pass

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
