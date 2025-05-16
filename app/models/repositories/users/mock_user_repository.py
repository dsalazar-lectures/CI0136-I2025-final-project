from ...services.user_repository_interface import IUserRepository

class MockUserRepository(IUserRepository):
    """
    Mock implementation of the user repository interface.
    
    This class provides an in-memory implementation of the user repository
    for testing and development purposes.
    """
    def __init__(self):
        """
        Initialize the mock repository with a default admin user.
        """
        self.users = {
            "admin@example.com": {
                "password": "Admin1@@@@@",
                "id": 1,
                "role": "Student"
            }
        }
        self.next_id = 2

    def get_user_by_email(self, email):
        """
        Retrieves a user by their email address.
        
        Args:
            email (str): The email address of the user to find
            
        Returns:
            dict: The user data if found, None otherwise
        """
        return self.users.get(email)

    def add_user(self, email, password, role):
        """
        Adds a new user to the repository.
        
        Args:
            email (str): The email address of the new user
            password (str): The password for the new user
            role (str): The role of the new user
            
        Returns:
            dict: The newly created user data
        """
        self.users[email] = {
            "password": password,
            "id": self.next_id,
            "role": role
        }
        self.next_id += 1
        return self.users[email]


    def user_exists(self, email):
        """
        Checks if a user with the given email exists.
        
        Args:
            email (str): The email address to check
            
        Returns:
            bool: True if user exists, False otherwise
        """
        return email in self.users
