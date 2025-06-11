"""
Authentication controller module.

This module defines routes and handlers for authentication-related functionality.
"""
from flask import Blueprint, flash, redirect, render_template, request, session, url_for, make_response
from ..models.repositories.users.firebase_user_repository import FirebaseUserRepository
# from app.models.repositories.users.mock_user_repository import MockUserRepository
from ..models.services.registration_service import validate_registration_data, validate_login_data
from app.services.notification import send_email_notification
from firebase_admin import auth as firebase_auth
from app.models.repositories.users.firebase_user_repository import FirebaseUserRepository
from firebase_admin import auth as firebase_auth
import traceback

# Create a Blueprint for home-related routes
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
# Repository for retrieving and storing user data
user_repo = FirebaseUserRepository()
# user_repo = MockUserRepository()


@auth_bp.route("/login", methods=("GET", "POST"))
def login():
    """
    Handle user login requests.

    For POST requests:
    - Validates login data
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
        user, error = validate_login_data(email, password, user_repo)
        # If any error occurs during validation, flash the error message and redirect to login page
        if error:
            flash(error, "danger")
            return redirect(url_for("auth.login"))
        # Otherwise, set session variables and redirect to home page
        session.pop('form_data', None)
        session.clear()
        session["user_id"] = user["id"]
        session["name"] = user.get("name", email)
        session["role"] = user["role"]
        session["email"] = email 

        # Send a login notification email
        # Prepare email data for notification
        email_data = {
            "username": session["name"],
            "emailTo": session["email"],
        }
        
        # Attempt to send the email notification
        if not send_email_notification("login", email_data):
            # (TODO) If email sending fails, log the error
            pass

        return redirect(url_for("home.home"))

    # Handle GET request - display registration form
    form_data = session.pop('form_data', {})
    response = make_response(render_template("login.html", form_data=form_data))
    # Set cache control headers to prevent form caching
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
    response.headers["Pragma"] = "no-cache"
    return response


@auth_bp.route("/logout", methods=["POST"])
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("auth.login"))
    
@auth_bp.route("/google-login", methods=["POST"])
def google_login():
    try:
        data = request.get_json()
        id_token = data.get("token")
        print("📨 ID Token recibido:", id_token)

        decoded_token = firebase_auth.verify_id_token(id_token)
        email = decoded_token.get("email")
        name = decoded_token.get("name", email)

        user_repo = FirebaseUserRepository()
        existing_user = user_repo.get_user_by_email(email)

        if not existing_user:
            print("📢 Usuario no existe, creando...")
            user_repo.add_user(
                name=name,
                email=email,
                password=None,
                role="student"
            )

        session.clear()
        session["user_id"] = existing_user["id"] if existing_user else 0  # o un valor por defecto
        session["email"] = email
        session["name"] = name
        session["role"] = existing_user["role"] if existing_user else "student"

        print("✅ Usuario autenticado con Google:", session["email"])
        return {"message": "Login con Google exitoso"}, 200

    except Exception as e:
        print("❌ Error en login con Google:")
        traceback.print_exc()
        return {"error": str(e)}, 500