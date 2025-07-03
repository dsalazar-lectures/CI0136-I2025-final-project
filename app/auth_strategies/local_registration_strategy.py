"""
Local Registration Strategy Module.

This module implements the local (email/password) registration strategy.
"""
from typing import Tuple, Dict, Any, Optional
import bcrypt
from flask import url_for
from ..auth_strategies.registration_strategy import RegistrationStrategy
from ..models.services.registration_service import validate_registration_data
from app.services.notification import send_email_notification
from app.services.audit import log_audit, AuditActionType

class LocalRegistrationStrategy(RegistrationStrategy):
    """
    Strategy for registering users with email and password.
    """
    
    def authenticate(self, user_data: Dict[str, Any], user_repo) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Register a user using name, email, password, and role.
        
        Args:
            user_data: Dictionary containing registration data (name, email, password, role).
            user_repo: Repository object for user data operations.
            
        Returns:
            A tuple containing (user_data, error_message).
        """
        name = user_data.get('name')
        email = user_data.get('email')
        password = user_data.get('password')
        role = user_data.get('role')
        
        # Check if user already exists with Google auth
        existing_user = user_repo.get_user_by_email(email)
        if existing_user and existing_user.get('auth_provider') == 'google':
            return None, "Este email ya está registrado mediante Google. Por favor inicia sesión con Google."
        
        # Validate registration data
        error_message, error_category = validate_registration_data(name, email, password, role, user_repo)
        if error_message:
            return None, error_message
            
        # Hash the password before storing
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Create the new user in the repository
        new_user = user_repo.add_user(name, email, hashed_password, role)
        
        # If user creation fails
        if not new_user:
            return None, "No se pudo crear el usuario. Es posible que ya exista con este email."
            
        # Set auth provider
        new_user['auth_provider'] = 'local'
        
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
            
        # Clear session data
        session.pop('form_data', None)
        
        return {
            'message': 'Registration successful. You can now log in.',
            'category': 'success',
            'redirect_url': url_for("auth.login")
        }
