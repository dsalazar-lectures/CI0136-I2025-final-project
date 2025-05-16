# """
# Profile controller module.

# This module defines the route to display the authenticated user's profile.
# """

# from flask import Blueprint, render_template, redirect, session, url_for

# # Blueprint for profile-related routes
# profile_bp = Blueprint("profile", __name__, url_prefix="/profile")


# @profile_bp.route("/", methods=["GET"])
# def view_profile():
#     """
#     Display the user's profile if authenticated.

#     Returns:
#         - Rendered profile template with user's name and role.
#         - Redirect to login if not authenticated.
#     """
#     # Authentication check
#     if "user_id" not in session or "role" not in session or "name" not in session:
#         return redirect(url_for("auth.login"))

#     # Retrieve user data from session
#     name = session["name"]
#     role = session["role"]

#     return render_template("profile.html", name=name, role=role)
"""
Profile controller module.

This module defines the route to display the authenticated user's profile.
"""

from flask import Blueprint, render_template

profile_bp = Blueprint("profile", __name__, url_prefix="/profile")


@profile_bp.route("/", methods=["GET"])
def view_profile():
    """
    Display a mock user's profile temporarily (no authentication).

    Returns:
        - Rendered profile template with mock name and role.
    """
    name = "Andrés Murillo"
    role = "Estudiante"

    return render_template("profile.html", name=name, role=role)
