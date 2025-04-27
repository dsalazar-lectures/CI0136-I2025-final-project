from abc import ABC, abstractmethod

class IUserRepository(ABC):
    
    @abstractmethod
    def get_user_by_email(self, email):
        pass

    @abstractmethod
    def add_user(self, email, password, role):
        pass

    @abstractmethod
    def user_exists(self, email):
        pass
