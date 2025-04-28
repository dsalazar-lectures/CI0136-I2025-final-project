from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    """
    Decorator to enforce user authentication for a route.

    Checks if the "user_id" key exists in the session.
    If the user is not logged in , it redirects the user
    to the login page. Otherwise, it allows the decorated
    function to execute.

    Args:
        f (function): The route handler function to be decorated.

    Returns:
        function: The decorated function that enforces login requirements.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function