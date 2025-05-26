
# Auth Decorator Manual:

## Overview

This document explains the structure, purpose, and usage of the `login_or_role_required` decorator, used for authentication and optional role-based access control in a Flask application.

This decorator ensures that only authenticated users those with specific roles can access certain routes.

---

## Importing the Decorator

To use the decorator in any Flask route handler, import it as follows:

```python
from app.utils.auth import login_or_role_required
```

---

## Function Definition

```python
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
```

---

## Usage Examples

### Authentication Only

Use this form when any authenticated user is allowed to access the route:

```python
@app.route("/dashboard")
@login_or_role_required()
def dashboard():
    return render_template("dashboard.html")
```

### Authentication + Role Validation

Use this form when only users with a specific role (e.g., `"Admin"`) are allowed:

```python
@app.route("/admin")
@login_or_role_required("Admin")
def admin_panel():
    return render_template("admin_panel.html")
```

---

## Session Requirements

To work correctly, the following keys must be present in the Flask `session` object:

```python
session = {
    "user_id": "abc123",  # User ID is required for all access
    "role": "Admin"       # Role is required only when validated
}
```

---

## Behavior Summary

| Condition                         | Behavior                         |
|----------------------------------|----------------------------------|
| No `user_id` in session          | Redirects to login page          |
| Role required but not matched    | Returns HTTP 403 Forbidden       |
| Role matched or not required     | Allows access to the route       |

---

## Best Practices

- Always place the decorator **below** `@app.route` and **above** the route function.
- Do not hardcode role values inside business logic; use the decorator for clarity.

---

## Additional Note
- In future sprint constants for each role will be implemented to avoid typos, for good practice. 