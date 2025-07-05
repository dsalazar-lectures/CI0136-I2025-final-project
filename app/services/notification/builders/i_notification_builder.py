# Biblioteca para la clase abstracta
from abc import ABC, abstractmethod

# Clase abstracta para las notificaciones de tipo email
class IBuilder(ABC):
  @abstractmethod
  def build_body(self, data: dict) -> dict:
    pass

  def get_bypass_priority(self):
    return self.always_notify
