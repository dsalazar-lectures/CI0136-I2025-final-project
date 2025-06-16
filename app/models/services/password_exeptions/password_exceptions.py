class PasswordValidationError(Exception):
    """Raised when the current password is incorrect"""
    pass

class PasswordUpdateError(Exception):
    """Raised when the new password could not be stored"""
    pass
