# Biblioteca para la clase abstracta
from abc import ABC, abstractmethod

# Acceso a los builders
from builders import Builder

# Clase abstracta para las fabricas
class BuilderFactory(ABC):
  @abstractmethod
  def create_builder(self, builder_type: str) -> Builder:
    pass

