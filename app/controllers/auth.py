from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flask import make_response

bp = Blueprint("auth", __name__)

# Hardcoded user list
users = {
    "admin@example.com": {
        "password": "Admin1@",  
        "id": 1,
        "role": "Student"
    }
}

@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        error = None
        # User validation 
        if email not in users or users[email]["password"] != password:
            error = "Invalid credentials."

        if error is None:
            session["user_id"] = users[email]["id"]
            session["role"] = users[email]["role"]
            flash("Login successful.", "success")
            return redirect(url_for("auth.home"))

        flash(error, "danger")
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