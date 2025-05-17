"""
Authentication controller module.

This module defines routes and handlers for authentication-related functionality.
"""
from flask import Blueprint, flash, redirect, render_template, request, session, url_for, make_response
from ..models.repositories.users.firebase_user_repository import FirebaseUserRepository
# from app.models.repositories.users.mock_user_repository import MockUserRepository
from ..models.services.registration_service import validate_registration_data, validate_login_data

# Create a Blueprint for home-related routes
auth_bp = Blueprint("auth", __name__)
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