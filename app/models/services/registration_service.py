"""
User registration and authentication services.

This module provides functions to validate user registration data
and authenticate user login credentials.
"""
from ...utils.utils import validate_name, validate_email, validate_password, validate_max_length
import bcrypt

def validate_registration_data(name, email, password, role, user_repo):
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

    if not name or not email or not password:
        return 'All fields are required.', 'danger'
    
    
    MAX_LENGTH = 100
    
    if not validate_max_length(name, MAX_LENGTH):
        return f'Name cannot exceed {MAX_LENGTH} characters.', 'danger'
        
    if not validate_max_length(email, MAX_LENGTH):
        return f'Email cannot exceed {MAX_LENGTH} characters.', 'danger'
        
    if not validate_max_length(password, MAX_LENGTH):
        return f'Password cannot exceed {MAX_LENGTH} characters.', 'danger'
    
    if not validate_name(name):
        return 'Invalid name.', 'danger'

    if not validate_email(email):
        return 'Invalid email.', 'danger'

    if not validate_password(password):
        return 'Password must include at least one uppercase letter, one number, and one special character.', 'danger'

    if len(password) < 8:
        return 'Password must be at least eight characters long.', 'danger'

    VALID_ROLES = {"Student", "Administrator", "Tutor"}
    if role not in VALID_ROLES:
        return "Invalid role selected. Must be Student, Administrator, or Tutor.", "danger"

    
    existing_user = user_repo.get_user_by_email(email)
    if existing_user:
        
        if existing_user.get('auth_provider') == 'google':
            return 'Este email ya está registrado mediante Google. Por favor inicia sesión con Google.', 'danger'
        else:
            return 'Este email ya está registrado. Por favor inicia sesión o utiliza otro email.', 'danger'

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
    
    MAX_LENGTH = 100
    
    if not validate_max_length(email, MAX_LENGTH) or not validate_max_length(password, MAX_LENGTH):
        return None, "Input fields exceed maximum allowed length of 100 characters."
    
    user = user_repo.get_user_by_email(email)

    if user is None or not user.get("password"):
        
        if user and user.get("auth_provider") == "google":
            return None, "Esta cuenta está registrada con Google. Por favor usa el botón 'Iniciar sesión con Google'."
        return None, "Invalid credentials."

    try:
        if bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
            return user, None
        else:
            return None, "Invalid credentials."
    except Exception:
        return None, "Invalid credentials."