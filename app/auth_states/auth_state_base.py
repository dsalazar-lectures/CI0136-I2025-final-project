"""
Auth State Abstract Class Module.

This module defines the abstract interface for authentication states.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple, Optional

class AuthState(ABC):
    """
    Abstract State base class for authentication.
    
    This defines the interface for different authentication state implementations.
    """
    
    @abstractmethod
    def login(self, credentials: Dict[str, Any], user_repo) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Authenticate a user using the provided credentials.
        
        Args:
            credentials: Dictionary containing authentication credentials.
            user_repo: Repository object for user data operations.
            
        Returns:
            A tuple containing (user_data, error_message).
        """
        pass
    
    @abstractmethod
    def setup_session(self, user: Dict[str, Any], session_obj) -> None:
        """
        Set up the user session after successful authentication.
        
        Args:
            user: User data dictionary.
            session_obj: Flask session object.
        """
        pass
    
    @abstractmethod
    def google_login(self, token: str, user_repo) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Authenticate a user using Google authentication.
        
        Args:
            token: Google ID token.
            user_repo: Repository object for user data operations.
            
        Returns:
            A tuple containing (user_data, error_message).
        """
        pass
