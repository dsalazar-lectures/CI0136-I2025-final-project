from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flask import make_response

bp = Blueprint("auth", __name__)

# Hardcoded user list
users = {
    "admin@example.com": {
        "password": "admin123",  # must be between 6 and 20 characters
        "id": 1,
        "role": "student"
    },
    "user@example.com": {
        "password": "userpass",
        "id": 2,
        "role": "student"
    }
}

@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None

        # Validations
        if username not in users:
            error = "User does not exist."
        elif len(password) < 6 or len(password) > 20:
            error = "Password must be between 6 and 20 characters long."
        elif users[username]["password"] != password:
            error = "Incorrect password."

        if error is None:
            session["user_id"] = users[username]["id"]
            session["role"] = users[username]["role"]
            flash("Login successful.")
            return redirect(url_for("auth.home"))

        flash(error)
        return redirect(url_for("auth.login"))

    response = make_response(render_template("login.html"))
    # Prevent browser caching of the login page to avoid displaying old flash messages
    # when the user presses the "Back" button after logging in or submitting the form.
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
    response.headers["Pragma"] = "no-cache"
    return response

@bp.route("/home")
def home():
    return render_template("home.html")