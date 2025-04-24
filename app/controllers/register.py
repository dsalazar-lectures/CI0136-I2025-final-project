from flask import Blueprint, render_template, request, redirect, flash, session, url_for, make_response

register_bp = Blueprint('register', __name__, url_prefix='/register')

# Simulated user list
users = [
    {'email': 'admin@example.com'}
]

@register_bp.route('/', methods=['GET', 'POST'])
def register():
    """
    Handles user registration.

    Routes:
    - GET: Renders the registration form.
    - POST: Processes registration form submission.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate input fields
        if not email or not password:
            flash('All fields are required.')
            return redirect(url_for('register.register'))

        # Check if email is already registered
        if any(user['email'] == email for user in users):
            flash('This email is already registered.')
            return redirect(url_for('register.register'))

        # Simulate saving user
        users.append({'email': email})
        flash('User registered successfully (simulated).')
        session.clear()

        # Redirect to greeting/home page
        return redirect(url_for("home.greeting"))

    # Render the registration form with no-cache headers
    response = make_response(render_template('register.html'))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
    response.headers["Pragma"] = "no-cache"
    return response
