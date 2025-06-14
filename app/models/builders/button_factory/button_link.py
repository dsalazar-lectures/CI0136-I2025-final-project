from abc import ABC, abstractmethod

class ButtonLink(ABC):
    
    @abstractmethod
    def render(self):
        pass

   