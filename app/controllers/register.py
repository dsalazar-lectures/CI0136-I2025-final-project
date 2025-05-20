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

# Create a Blueprint for registration-related routes
register_bp = Blueprint('register', __name__, url_prefix='/register')
# Repository for retrieving and storing user data
# user_repo = MockUserRepository() 
user_repo = FirebaseUserRepository()
@register_bp.route('/', methods=['GET', 'POST'])
def register():
    """
    Handle user registration requests.
    
    For POST requests:
    - Validates registration data
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
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        # Store form data in session for form repopulation in case of errors
        session['form_data'] = {
            'email': email,
            'password': password,
            'role': role
        }
        error_message, error_category = validate_registration_data(email, password, role, user_repo)

        if error_message:
            flash(error_message, error_category)
            return redirect(url_for('register.register'))
        # Create new user and clear session data
        user_repo.add_user(email, password, role)
        session.pop('form_data', None)
        session.clear()
        # Notify user of successful registration and redirect to login
        flash('Registration successful. You can now log in.', 'success')
        return redirect(url_for("auth.login"))

    # Handle GET request - display registration form
    form_data = session.pop('form_data', {})
    response = make_response(render_template('register.html', form_data=form_data))
    # Set cache control headers to prevent form caching
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
    response.headers["Pragma"] = "no-cache"
    return response
