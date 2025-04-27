from flask import Blueprint, flash, redirect, render_template, request, session, url_for, make_response
from ..models.repositories.mock_user_repository import MockUserRepository
from ..models.services.registration_service import validate_registration_data, validate_login_data

auth_bp = Blueprint("auth", __name__)
user_repo = MockUserRepository()

@auth_bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        session['form_data'] = {
            'email': email,
            'password': password,
        }

        user, error = validate_login_data(email, password, user_repo)

        if error:
            flash(error, "danger")
            return redirect(url_for("auth.login"))

        session["user_id"] = user["id"]
        session["role"] = user["role"]
        flash("Login successful.", "success")
        return redirect(url_for("home.home"))

    form_data = session.pop('form_data', {})
    response = make_response(render_template("login.html", form_data=form_data))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
    response.headers["Pragma"] = "no-cache"
    return response
