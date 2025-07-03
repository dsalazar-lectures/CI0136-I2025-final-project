"""
Google Registration Strategy Module.

This module implements the Google OAuth registration strategy.
"""
from typing import Tuple, Dict, Any, Optional
from flask import url_for
from ..auth_strategies.registration_strategy import RegistrationStrategy
from app.services.notification import send_email_notification
from app.services.audit import log_audit, AuditActionType

class GoogleRegistrationStrategy(RegistrationStrategy):
    """
    Strategy for registering users with Google OAuth.
    """
    
    def authenticate(self, user_data: Dict[str, Any], user_repo) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Register a user using Google OAuth data.
        
        Args:
            user_data: Dictionary containing Google user data (name, email).
            user_repo: Repository object for user data operations.
            
        Returns:
            A tuple containing (user_data, error_message).
        """
        name = user_data.get('name')
        email = user_data.get('email')
        role = user_data.get('role', 'Student')  # Default role for Google registrations
        
        # Check if user already exists with local auth
        existing_user = user_repo.get_user_by_email(email)
        if existing_user:
            if existing_user.get('auth_provider') != 'google':
                # Link the accounts - in a real app, this might be more complex
                existing_user['auth_provider'] = 'google'
                return existing_user, None
            else:
                # User already exists with Google auth - this is a login, not a registration
                return existing_user, None
                
        # Create the new user in the repository
        new_user = user_repo.add_user(name, email, None, role)
        
        # If user creation fails
        if not new_user:
            return None, "No se pudo crear el usuario con Google."
            
        # Set auth provider
        new_user['auth_provider'] = 'google'
        
        return new_user, None
        
    def process_registration_result(self, user: Dict[str, Any], session) -> Dict[str, Any]:
        """
        Process the result of a successful registration.
        
        Args:
            user: User data dictionary.
            session: Flask session object.
            
        Returns:
            A dictionary with information about the registration process.
        """
        name = user.get('name')
        email = user.get('email')
        
        # Send a registration notification email
        email_data = {
            "username": name,
            "emailTo": email,
        }
        
        email_sent = send_email_notification("successRegister", email_data)
        if not email_sent:
            log_audit(
                user=name,
                action_type=AuditActionType.USER_REGISTER,
                details=f"Failed to send registration email to {email}"
            )
            
        # Clear form data from session if exists
        session.pop('form_data', None)
        
        # For Google registrations, usually they are automatically logged in
        # So we'll return a different message and redirect
        return {
            'message': 'Registration with Google successful.',
            'category': 'success',
            'redirect_url': url_for("home.home")
        }
