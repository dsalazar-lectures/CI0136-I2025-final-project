# Biblioteca para la clase abstracta
from abc import ABC, abstractmethod

# Acceso a los builders
from ..builders import *

# Clase abstracta para las fabricas
class IBuilderFactory(ABC):
  @abstractmethod
  def create_builder(self, builder_type: str) -> IBuilder:
    pass

