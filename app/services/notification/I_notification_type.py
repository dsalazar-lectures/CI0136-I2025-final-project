# Biblioteca para la clase abstracta
from abc import ABC, abstractmethod

# Clase abstracta para el servicio de notificaciones por correo electronico
class NotificationService(ABC):
  @abstractmethod
  def send(self, data: dict) -> bool:
    pass
