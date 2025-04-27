from flask import Blueprint, render_template, request, redirect, flash, session, url_for, make_response
from ..utils.utils import validate_email, validate_password
from ..models.repositories.mock_user_repository import MockUserRepository

register_bp = Blueprint('register', __name__, url_prefix='/register')
user_repo = MockUserRepository() 

@register_bp.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        # Save form fields
        session['form_data'] = {
            'email': email,
            'password': password,
            'role': role
        }

        # Validations
        if not email or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('register.register'))

        if not validate_email(email):  
            flash('Invalid email.', 'danger')
            return redirect(url_for('register.register'))

        if not validate_password(password): 
            flash('Password must include at least one uppercase letter, one number, and one special character.', 'danger')
            return redirect(url_for('register.register'))

        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return redirect(url_for('register.register'))

        if role != 'Student':
            flash('Role not available at the moment.', 'danger')
            return redirect(url_for('register.register'))

        if user_repo.user_exists(email):  # validate if the user exist
            flash('This email is already registered.', 'danger')
            return redirect(url_for('register.register'))

        # Add user to the repository
        user_repo.add_user(email, password, role) 

        flash('Registration successful. You can now log in.', 'success')
        return redirect(url_for("register.register")) 

    
    form_data = session.pop('form_data', {})
    response = make_response(render_template('register.html', form_data=form_data))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
    response.headers["Pragma"] = "no-cache"
    return response
