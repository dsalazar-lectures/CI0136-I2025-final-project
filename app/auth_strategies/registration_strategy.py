"""
Registration Strategy Module.

This module defines the abstract interface for registration strategies.
"""
from abc import ABC, abstractmethod
from typing import Tuple, Dict, Any, Optional

class RegistrationStrategy(ABC):
    """
    Base class for registration strategies.
    
    This abstract class defines the common interface that all
    registration strategies must implement.
    """
    
    @abstractmethod
    def authenticate(self, user_data: Dict[str, Any], user_repo) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Register a user using the provided data.
        
        Args:
            user_data: Dictionary containing registration data.
            user_repo: Repository object for user data operations.
            
        Returns:
            A tuple containing (user_data, error_message). If registration
            is successful, user_data contains the new user information and
            error_message is None. If registration fails, user_data is None
            and error_message contains the reason for failure.
        """
        pass
        
    @abstractmethod
    def process_registration_result(self, user: Dict[str, Any], session) -> Dict[str, Any]:
        """
        Process the result of a successful registration.
        
        Args:
            user: User data dictionary.
            session: Flask session object.
            
        Returns:
            A dictionary with information about the registration process,
            such as success messages, redirect URLs, etc.
        """
        pass
