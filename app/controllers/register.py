"""
Registration controller module.

This module handles user registration functionality, including form processing,
validation, and user creation.
"""
from flask import Blueprint, render_template, request, redirect, flash, session, url_for, make_response
# from ..models.repositories.users.mock_user_repository import MockUserRepository
# from app.models.repositories.users.mock_user_repository import MockUserRepository
from app.models.repositories.users.firebase_user_repository import FirebaseUserRepository
from ..models.services.registration_service import validate_registration_data
from app.services.notification import send_email_notification
from app.services.audit import log_audit, AuditActionType
import bcrypt
from firebase_admin import auth as firebase_auth
from ..auth_strategies.registration_strategy_factory import RegistrationStrategyFactory

# Create a Blueprint for registration-related routes
register_bp = Blueprint('register', __name__, url_prefix='/register')
# Repository for retrieving and storing user data
user_repo = FirebaseUserRepository()

@register_bp.route('/', methods=['GET', 'POST'])
def register():
    """
    Handle user registration requests.
    
    For POST requests:
    - Validates registration data using the local registration strategy
    - Creates a new user if validation passes
    - Redirects to login page on success
    - Redirects back to registration form with error message on failure
    
    For GET requests:
    - Renders the registration form and populates it with
    previous submission data if available
    
    Returns:
        For POST: Redirect to login or registration page
        For GET: Rendered registration form
    """
    if request.method == 'POST':
        # Extract form data
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        
        # Store form data in session for form repopulation in case of errors
        session['form_data'] = {
            'name': name,
            'email': email,
            'password': password,
            'role': role,
            'notification_enabled': True
        }
        
        # Get the local registration strategy
        registration_strategy = RegistrationStrategyFactory.create_strategy("local")
        user_data = {
            'name': name,
            'email': email,
            'password': password,
            'role': role,
            'notification_enabled': True
        }
        
        # Register the user
        new_user, error = registration_strategy.authenticate(user_data, user_repo)
        
        # If any error occurs during registration
        if error:
            flash(error, "danger")
            return redirect(url_for('register.register'))
            
        # Process the successful registration
        result = registration_strategy.process_registration_result(new_user, session)
        
        # Flash success message and redirect
        flash(result['message'], result['category'])

        log_audit(
                user=name,
                action_type=AuditActionType.USER_REGISTER,
                details=f"User registered successfully"
            )

        return redirect(result['redirect_url'])

    # Handle GET request - display registration form
    form_data = session.pop('form_data', {})
    response = make_response(render_template('register.html', form_data=form_data))
    # Set cache control headers to prevent form caching
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
    response.headers["Pragma"] = "no-cache"
    return response

@register_bp.route('/google', methods=['POST'])
def google_register():
    """
    Handle registration with Google.
    
    For POST requests:
    - Processes Google OAuth data
    - Creates a new user or links with existing account
    - Returns a JSON response with result
    
    Returns:
        JSON response with success/error message
    """
    try:
        data = request.get_json()
        token = data.get('token')
        
        if not token:
            return {'error': 'No token provided'}, 400
            
        # Decode token to get user info
        decoded_token = firebase_auth.verify_id_token(token)
        email = decoded_token.get('email')
        name = decoded_token.get('name', email)
        
        # Get the Google registration strategy
        registration_strategy = RegistrationStrategyFactory.create_strategy("google")
        user_data = {
            'name': name,
            'email': email,
            'role': 'Student'  # Default role for Google registrations
        }
        
        # Register/login the user
        user, error = registration_strategy.authenticate(user_data, user_repo)
        
        # If any error occurs during registration
        if error:
            return {'error': error}, 400
            
        # Process the successful registration
        result = registration_strategy.process_registration_result(user, session)
        
        return {'message': result['message'], 'redirect_url': result['redirect_url']}, 200
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {'error': str(e)}, 500
