from functools import wraps
from flask import session, abort

def login_and_role_required(required_role):
    """
    Decorator to enforce user authentication and role-based access control for a route.

    Args:
        required_role (str): The role required to access the route.

    Returns:
        Function: The wrapped function that enforces login and role requirements.
    """
    def decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            # Check if the user is logged in
            if "user_id" not in session:
                abort(403)  # Return a 403 Forbidden error if not logged in
            # Check if the user has the required role
            if "role" not in session or session["role"] != required_role:
                abort(403)  # Return a 403 Forbidden error if role doesn't match
            return func(*args, **kwargs)
        return wrapped_function
    return decorator
