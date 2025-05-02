class UserError(Exception):
    """Base class for user-related exceptions."""
    pass

class InvalidEmailError(UserError):
    """Raised when the email format is invalid."""
    pass

class MissingEmailError(UserError):
    """Raised when the email is required but missing."""
    pass

class InvalidPasswordError(UserError):
    """Raised when the password does not meet complexity requirements."""
    pass

class MissingPasswordError(UserError):
    """Raised when the password is required but missing."""
    pass

class InvalidPhoneNumberError(UserError):
    """Raised when the phone number format is invalid."""
    pass