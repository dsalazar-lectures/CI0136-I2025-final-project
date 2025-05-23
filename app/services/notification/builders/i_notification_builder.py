# Biblioteca para la clase abstracta
from abc import ABC, abstractmethod

# Clase abstracta para las notificaciones de tipo email
class Builder(ABC):
  @abstractmethod
  def buildBody(self, data: dict) -> dict:
    pass
