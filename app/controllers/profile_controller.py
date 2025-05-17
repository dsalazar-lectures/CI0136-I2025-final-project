from flask import Blueprint, render_template, session, redirect, url_for, request, flash

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
    name = session.get("name", "Usuario")
    email = session.get("email", f"{user_id}@example.com")

    return render_template("profile.html", name=name, role=role, email=email)


@profile_bp.route("/edit", methods=["POST"])
def edit_profile():
    """
    Handle profile edits for name and role.
    """
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    # Get form data
    new_name = request.form.get("name", "").strip()
    new_role = request.form.get("role", "").strip()

    if not new_name or not new_role:
        flash("Name and role are required.", "danger")
        return redirect(url_for("profile.view_profile"))

    session["name"] = new_name
    session["role"] = new_role

    flash("Profile updated successfully.", "success")
    return redirect(url_for("profile.view_profile"))
