from flask import Blueprint, render_template, request, redirect, flash, session, url_for, make_response
from ..models.repositories.mock_user_repository import MockUserRepository
from ..models.services.registration_service import validate_registration_data

register_bp = Blueprint('register', __name__, url_prefix='/register')
user_repo = MockUserRepository() 

@register_bp.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        session['form_data'] = {
            'email': email,
            'password': password,
            'role': role
        }

        error_message, error_category = validate_registration_data(email, password, role, user_repo)

        if error_message:
            flash(error_message, error_category)
            return redirect(url_for('register.register'))

        user_repo.add_user(email, password, role)
        session.pop('form_data', None)
        session.clear()

        flash('Registration successful. You can now log in.', 'success')
        return redirect(url_for("auth.login"))

    form_data = session.pop('form_data', {})
    response = make_response(render_template('register.html', form_data=form_data))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
    response.headers["Pragma"] = "no-cache"
    return response
