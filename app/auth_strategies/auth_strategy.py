"""
Auth Strategy Module.

This module defines the abstract interface for authentication strategies.
"""
from abc import ABC, abstractmethod
from typing import Tuple, Dict, Any, Optional

class AuthStrategy(ABC):
    """
    Base class for authentication strategies.
    
    This abstract class defines the common interface that all
    authentication strategies must implement.
    """
    
    @abstractmethod
    def authenticate(self, credentials: Dict[str, Any], user_repo) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Authenticate a user using the provided credentials.
        
        Args:
            credentials: Dictionary containing authentication credentials.
            user_repo: Repository object for user data operations.
            
        Returns:
            A tuple containing (user_data, error_message). If authentication
            is successful, user_data contains the user information and
            error_message is None. If authentication fails, user_data is None
            and error_message contains the reason for failure.
        """
        pass
        
    @abstractmethod
    def setup_session(self, user: Dict[str, Any], session) -> None:
        """
        Setup the session for an authenticated user.
        
        Args:
            user: User data dictionary.
            session: Flask session object.
        """
        pass
