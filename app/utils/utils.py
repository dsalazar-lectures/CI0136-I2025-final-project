import re

def validate_name(name):
    """
    Validates a name against a specific regex pattern.

    The name must:
    - Start with an uppercase letter.
    - Contain only letters, spaces, and hyphens.
    - Be between 2 and 50 characters long.

    Args:
        name (str): The name string to validate.

    Returns:
        re.Match or None: A match object if the name meets the criteria,
                          or None if it does not.
    """
    name_regex = r'^[A-Z][a-zA-Z\s-]{1,49}$'
    return re.match(name_regex, name)

def validate_email(email):
    """
    Validates an email address against a specific regex pattern.

    The email must:
    - Start with alphanumeric characters, underscores, dots, or plus signs.
    - Contain an '@' symbol followed by a domain name.
    - End with a valid domain suffix.

    Args:
        email (str): The email address string to validate.

    Returns:
        re.Match or None: A match object if the email meets the criteria,
                          or None if it does not.
    """
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email)

def validate_password(password):
    """
    Validates a password against a specific set of criteria.

    The password must:
    - Contain at least one uppercase letter.
    - Contain at least one digit.
    - Contain at least one special character from the set @$!%*?&.
    - Consist only of alphanumeric characters and the specified special characters.

    Args:
        password (str): The password string to validate.

    Returns:
        re.Match or None: A match object if the password meets the criteria, 
                          or None if it does not.
    """
    password_regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$'
    return re.match(password_regex, password)
