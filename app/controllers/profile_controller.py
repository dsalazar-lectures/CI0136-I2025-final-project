from flask import Blueprint, render_template, session, redirect, url_for

profile_bp = Blueprint("profile", __name__, url_prefix="/profile")

@profile_bp.route("/", methods=["GET"])
def view_profile():
    """
    Display the logged-in user's profile.

    Returns:
        - Rendered profile template with user's session data.
        - Redirect to login if user is not authenticated.
    """
    if "user_id" not in session or "role" not in session:
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]
    role = session["role"]
    name = "Usuario" 
    email = session.get("email", f"{user_id}@example.com")

    return render_template("profile.html", name=name, role=role, email=email)
