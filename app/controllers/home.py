"""
Home controller module.

This module defines routes and handlers for the home page of the application.
"""
from flask import Blueprint, render_template
from ..utils.auth import login_required

# Create a Blueprint for home-related routes
home_bp = Blueprint('home', __name__)

@home_bp.route("/")
@login_required
def home():
    """
    Render the home page.
    
    This route is protected and requires user authentication.
    
    Returns:
        Rendered home.html template document.
    """
    return render_template("home.html")