from functools import wraps
from flask import session, abort, redirect, url_for

def login_or_role_required(required_role=None):
    """
    Decorator to enforce user authentication and (optionally) role-based access control.

    Args:
        required_role (str or None): The role required to access the route, or None for any logged-in user.

    Returns:
        Function: The wrapped function that enforces login and role requirements.
    """
    def decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            # Check if the user is logged in
            if "user_id" not in session:
                return redirect(url_for("auth.login"))
            # If a role is required, check it
            if required_role is not None:
                if "role" not in session or session["role"] != required_role:
                    abort(403)
            return func(*args, **kwargs)
        return wrapped_function
    return decorator
