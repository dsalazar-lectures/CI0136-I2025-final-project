# Biblioteca para la clase abstracta
from abc import ABC, abstractmethod

# Acceso a los builders
from app.services.notification.builders.I_notification_builder import Builder

# Clase abstracta para las fabricas
class BuilderFactory(ABC):
  @abstractmethod
  def createBody(self, builderType: str, datos) -> Builder:
    pass

