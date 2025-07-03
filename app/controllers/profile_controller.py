from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from ..utils.auth import login_or_role_required
from ..models.repositories.users.firebase_user_repository import FirebaseUserRepository
from ..models.repositories.tutorial.firebase_tutorings_repository import FirebaseTutoringRepository
from ..utils.utils import validate_max_length  # Importamos la función de validación

profile_bp = Blueprint("profile", __name__, url_prefix="/profile")
user_repo = FirebaseUserRepository()
tutoring_repo = FirebaseTutoringRepository()

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
    notification_enabled = session.get("notification_enabled")
    tutorias = []

    try:
        user_data = user_repo.get_user_by_email(email)
        if user_data and 'profile_picture_url' in user_data:
            profile_url = user_data['profile_picture_url']
            
            if 'drive.google.com' in profile_url and 'thumbnail' not in profile_url:
                # Extract file ID from various Google Drive URL formats
                if '/uc?export=view&id=' in profile_url:
                    file_id = profile_url.split('/id=')[1].split('&')[0]
                elif '/uc?id=' in profile_url:
                    file_id = profile_url.split('/id=')[1].split('&')[0]
                elif '/file/d/' in profile_url:
                    file_id = profile_url.split('/file/d/')[1].split('/')[0]
                else:
                    file_id = None
                
                if file_id:
                    profile_url = f"https://drive.google.com/thumbnail?id={file_id}&sz=w400-h400"
                    print(f"Converted profile picture URL to thumbnail format: {profile_url}")
            
            session['profile_picture_url'] = profile_url
            print(f"Loaded profile picture from Firebase: {profile_url}")
        else:
            print(f"No profile picture found in Firebase for user: {email}")
    except Exception as e:
        print(f"Error loading user profile picture: {e}")

    if session.get('role') == 'Tutor':
        tutor_id = session.get('user_id')
        tutorias = tutoring_repo.get_tutorials_by_tutor(tutor_id)

    return render_template("profile.html", name=name, role=role, email=email, tutorias=tutorias, notification_enabled=notification_enabled)

@profile_bp.route("/edit", methods=["POST"])
def edit_profile():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    new_name = request.form.get("name", "").strip()
    new_role = request.form.get("role", "").strip()
    new_profile_picture_url = request.form.get("profile_picture_url", "").strip()

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
    
    update_data = {
        "name": new_name,
        "role": new_role
    }
    
    # Save profile picture URL if provided
    if new_profile_picture_url:
        if 'drive.google.com' in new_profile_picture_url and 'thumbnail' not in new_profile_picture_url:
            if '/uc?export=view&id=' in new_profile_picture_url:
                file_id = new_profile_picture_url.split('/id=')[1].split('&')[0]
            elif '/uc?id=' in new_profile_picture_url:
                file_id = new_profile_picture_url.split('/id=')[1].split('&')[0]
            elif '/file/d/' in new_profile_picture_url:
                file_id = new_profile_picture_url.split('/file/d/')[1].split('/')[0]
            else:
                file_id = None
            
            if file_id:
                new_profile_picture_url = f"https://drive.google.com/thumbnail?id={file_id}&sz=w400-h400"
                print(f"Converted profile picture URL to thumbnail format for saving: {new_profile_picture_url}")
        
        update_data['profile_picture_url'] = new_profile_picture_url
        session['profile_picture_url'] = new_profile_picture_url
        print(f"Saving profile picture URL to Firebase: {new_profile_picture_url}")
    
    if 'temp_profile_picture_url' in session:
        del session['temp_profile_picture_url']
    
    try:
        user_repo.update_user_fields(session["email"], update_data)
        print(f"Successfully updated user profile in Firebase")
        flash("Profile updated successfully.", "success")
    except Exception as e:
        print(f"Error updating user profile: {e}")
        flash("Error updating profile. Please try again.", "danger")
        return render_template(
            "profile.html",
            name=session["name"],
            role=session["role"],
            email=session.get("email", ""),
            show_modal=True  
        )
    
    return redirect(url_for("profile.view_profile"))