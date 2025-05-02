from ...domain.exceptions.user_exceptions import UserError


class UniqueFieldAlreadyTaken(UserError):
    """Raised when the email format is invalid."""
    pass