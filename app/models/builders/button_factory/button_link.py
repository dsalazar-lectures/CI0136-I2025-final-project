from abc import ABC, abstractmethod

class ButtonLink(ABC):
    
    @abstractmethod
    def render_access_button(self):
        pass

   