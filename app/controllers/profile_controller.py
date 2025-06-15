from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from ..models.repositories.users.firebase_user_repository import FirebaseUserRepository
from ..utils.utils import validate_max_length  # Importamos la función de validación

profile_bp = Blueprint("profile", __name__, url_prefix="/profile")
user_repo = FirebaseUserRepository()

@profile_bp.route("/", methods=["GET"])
def view_profile():
    """
    Display the logged-in user's profile.
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
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    new_name = request.form.get("name", "").strip()
    new_role = request.form.get("role", "").strip()

    if not new_name or not new_role:
        flash("Name and role are required.", "danger")
        return render_template(
            "profile.html",
            name=session["name"],
            role=session["role"],
            email=session.get("email", ""),
            show_modal=True  
        )
    
    MAX_LENGTH = 100
    
    if not validate_max_length(new_name, MAX_LENGTH):
        flash(f"Name cannot exceed {MAX_LENGTH} characters.", "danger")
        return render_template(
            "profile.html",
            name=session["name"],
            role=session["role"],
            email=session.get("email", ""),
            show_modal=True  
        )
    
    VALID_ROLES = {"Student", "Administrator", "Tutor"}
    if new_role not in VALID_ROLES:
        flash("Invalid role selected. Must be Student, Administrator, or Tutor.", "danger")
        return render_template(
            "profile.html",
            name=session["name"],
            role=session["role"],
            email=session.get("email", ""),
            show_modal=True  
        )

    session["name"] = new_name
    session["role"] = new_role
    user_repo.update_user_fields(session["email"], {
        "name": new_name,
        "role": new_role
    })
    flash("Profile updated successfully.", "success")
    return redirect(url_for("profile.view_profile"))