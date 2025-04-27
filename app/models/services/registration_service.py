from ...utils.utils import validate_email, validate_password

def validate_registration_data(email, password, role, user_repo):
    if not email or not password:
        return 'All fields are required.', 'danger'

    if not validate_email(email):
        return 'Invalid email.', 'danger'

    if not validate_password(password):
        return 'Password must include at least one uppercase letter, one number, and one special character.', 'danger'

    if len(password) < 6:
        return 'Password must be at least 6 characters long.', 'danger'

    if role != 'Student':
        return 'Role not available at the moment.', 'danger'

    if user_repo.user_exists(email):
        return 'This email is already registered.', 'danger'

    return None, None

def validate_login_data(email, password, user_repo):
    user = user_repo.get_user_by_email(email)

    if user is None or user["password"] != password:
        return None, "Invalid credentials."

    return user, None