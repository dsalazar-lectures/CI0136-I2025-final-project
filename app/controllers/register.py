from flask import Blueprint, render_template, request, redirect, flash, session, url_for, make_response
import re

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
        role = request.form.get('role')

        # Flash form data to session
        session['form_data'] = {
            'email': email,
            'password': password,
            'role': role
        }

        # Validate input fields
        if not email or not password:
            flash('All fields are required.')
            return redirect(url_for('register.register'))
        
        # Validate email format
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            flash('Invalid email.')
            return redirect(url_for('register.register'))
       
        # Validate password complexity
        password_regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$'
        if not re.match(password_regex, password):
            flash('Password must include at least one uppercase letter, one number, and one special character.')
            return redirect(url_for('register.register'))
        
        # Validate password length
        if len(password) < 6:
            flash('Password must be at least 8 characters long.')

        # Validate available role
        if role != 'Student':
            flash('Role not available at the moment.')
            return redirect(url_for('register.register'))
        
        # Check if email is already registered
        if any(user['email'] == email for user in users):
            flash('This email is already registered.')
            return redirect(url_for('register.register'))

        # Simulate saving user
        users.append({'email': email, 'role': role})
        flash('User registered successfully (simulated).')
        session.pop('form_data', None)  # Clear form data after successful registration
        session.clear()

        # Redirect to greeting/home page
        return redirect(url_for("home.greeting"))

    # Render the registration form with no-cache headers
    form_data = session.pop('form_data', {}) 
    response = make_response(render_template('register.html', form_data=form_data))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
    response.headers["Pragma"] = "no-cache"
    return response
