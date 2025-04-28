from abc import ABC, abstractmethod

class IUserRepository(ABC):
    """
    Interface defining required methods for user repository implementations.
    
    This interface ensures that any user repository, regardless of underlying storage,
    implements the necessary methods for user management.
    """

    @abstractmethod
    def get_user_by_email(self, email):
        """
        Retrieves a user by their email address.
        
        Args:
            email (str): The email address of the user to find
            
        Returns:
            User: The user object if found, None otherwise
        """
        pass

    @abstractmethod
    def add_user(self, email, password, role):
        """
        Adds a new user to the repository.
        
        Args:
            email (str): The email address of the new user
            password (str): The password for the new user
            role (str): The role of the new user
            
        Returns:
            User: The newly created user object
        """
        pass

    @abstractmethod
    def user_exists(self, email):
        """
        Checks if a user with the given email exists.
        
        Args:
            email (str): The email address to check
            
        Returns:
            bool: True if user exists, False otherwise
        """
        pass
