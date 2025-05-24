# Biblioteca para la clase abstracta
from abc import ABC, abstractmethod

# Clase abstracta para el servicio de notificacion
class INotificationService(ABC):
  @abstractmethod
  def send(self, data: dict) -> bool:
    pass


