"""
Authentication controller module.

This module defines routes and handlers for authentication-related functionality.
"""
from flask import Blueprint, flash, redirect, render_template, request, session, url_for, make_response
from ..models.repositories.users.firebase_user_repository import FirebaseUserRepository
from app.services.notification import send_email_notification
import traceback
from ..auth_states.auth_state import AuthStateContext

# Create a Blueprint for home-related routes
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
# Repository for retrieving and storing user data
user_repo = FirebaseUserRepository()


@auth_bp.route("/login", methods=("GET", "POST"))
def login():
    """
    Handle user login requests.

    For POST requests:
    - Validates login data using the local authentication strategy
    - Sets session variables for user id and role on success
    - Redirects to home page on success
    - Redirects back to login page with error message on failure
    
    For GET requests:
    - Renders the login form and populates it with
    previous submission data if available
    
    Returns:
        For POST: Redirect to home page on success or login page on failure
        For GET: Rendered login form
    """
    if request.method == "POST":
        # Extract form data
        email = request.form["email"]
        password = request.form["password"]
        # Store form data in session for form repopulation in case of errors
        session['form_data'] = {
            'email': email,
            'password': password,
        }
        
        # Get the appropriate auth state based on environment configuration
        auth_state = AuthStateContext.get_state()
        credentials = {
            'email': email,
            'password': password
        }
        
        # Authenticate the user
        user, error = auth_state.login(credentials, user_repo)
        
        # If any error occurs during validation, flash the error message and redirect to login page
        if error:
            flash(error, "danger")
            return redirect(url_for("auth.login"))
            
        # Set up the session with user data
        session.pop('form_data', None)
        auth_state.setup_session(user, session)

        return redirect(url_for("home.home"))

    # Handle GET request - display registration form
    form_data = session.pop('form_data', {})
    response = make_response(render_template("login.html", form_data=form_data))
    # Set cache control headers to prevent form caching
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
    response.headers["Pragma"] = "no-cache"
    return response

@auth_bp.route("/google-login", methods=["POST"])
def google_login():
    try:
        data = request.get_json()
        id_token = data.get("token")
        
        # Get the appropriate auth state based on environment configuration
        auth_state = AuthStateContext.get_state()
        
        # Authenticate the user with Google
        user, error = auth_state.google_login(id_token, user_repo)
        
        # If any error occurs during authentication
        if error:
            print(f"Error en autenticación con Google: {error}")
            return {"error": error}, 400
            
        # Set up the session with user data
        auth_state.setup_session(user, session)

        print("Usuario autenticado con Google:", session["email"])
        return {"message": "Login con Google exitoso"}, 200

    except Exception as e:
        print("Error en login con Google:")
        traceback.print_exc()
        return {"error": str(e)}, 500


@auth_bp.route("/logout", methods=["POST"])
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("auth.login"))
    