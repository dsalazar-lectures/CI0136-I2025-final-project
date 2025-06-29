"""
Local Auth Strategy Module.

This module implements the local (email/password) authentication strategy.
"""
from typing import Tuple, Dict, Any, Optional
from flask import session
from ..auth_strategies.auth_strategy import AuthStrategy
from ..models.services.registration_service import validate_login_data
from app.services.notification import send_email_notification

class LocalAuthStrategy(AuthStrategy):
    """
    Strategy for authenticating users with email and password.
    """
    
    def authenticate(self, credentials: Dict[str, Any], user_repo) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Authenticate a user using email and password.
        
        Args:
            credentials: Dictionary containing 'email' and 'password'.
            user_repo: Repository object for user data operations.
            
        Returns:
            A tuple containing (user_data, error_message).
        """
        email = credentials.get('email')
        password = credentials.get('password')
        
        # Use the existing validation function
        user, error = validate_login_data(email, password, user_repo)
        return user, error
        
    def setup_session(self, user: Dict[str, Any], session) -> None:
        """
        Setup the session for a locally authenticated user.
        
        Args:
            user: User data dictionary.
            session: Flask session object.
        """
        email = user.get('email')
        
        # Clear any existing session data
        session.clear()
        
        # Set up the session with user data
        session["user_id"] = user["id"]
        session["name"] = user.get("name", email)
        session["role"] = user["role"]
        session["status"] = user.get("status")
        session["email"] = email
        session["notification_enabled"] = user["notification_enabled"]
        session["auth_provider"] = "local"
        
        # Send a login notification email
        email_data = {
            "username": session["name"],
            "emailTo": session["email"],
        }
        
        # Attempt to send the email notification
        send_email_notification("login", email_data)
