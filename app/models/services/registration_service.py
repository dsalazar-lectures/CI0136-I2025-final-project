"""
User registration and authentication services.

This module provides functions to validate user registration data
and authenticate user login credentials.
"""
from ...utils.utils import validate_email, validate_password

def validate_registration_data(email, password, role, user_repo):
    """
    Validates user registration data against business rules.
    
    Args:
        email (str): User's email address
        password (str): User's password
        role (str): User's role in the system
        user_repo (IUserRepository): Repository for user operations
        
    Returns:
        tuple: (error_message, category)
            - error_message (str): Description of validation error or None if valid
            - category (str): Error category ('danger') or None if valid
    """
    if not email or not password:
        return 'All fields are required.', 'danger'

    if not validate_email(email):
        return 'Invalid email.', 'danger'

    if not validate_password(password):
        return 'Password must include at least one uppercase letter, one number, and one special character.', 'danger'

    if len(password) < 8:
        return 'Password must be at least eight characters long.', 'danger'

    if role != 'Student':
        return 'Role not available at the moment.', 'danger'

    if user_repo.user_exists(email):
        return 'This email is already registered.', 'danger'

    return None, None

def validate_login_data(email, password, user_repo):
    """
    Validates user login credentials.
    
    Args:
        email (str): User's email address
        password (str): User's password
        user_repo (IUserRepository): Repository for user operations
        
    Returns:
        tuple: (user, error_message)
            - user (dict): User object if authentication successful, None otherwise
            - error_message (str): Error description if authentication failed, None otherwise
    """
    user = user_repo.get_user_by_email(email)

    if user is None or user["password"] != password:
        return None, "Invalid credentials."

    return user, None