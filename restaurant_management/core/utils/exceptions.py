from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

class PasswordValidationException(Exception):
    """Custom exception for password validation errors"""
    pass


class StockNotFoundError(Exception):
   def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class BuisnessLogicFailException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class RepositoryException(Exception):
    pass

def custom_exception_handler(exc, context):
    """
    Custom exception handler for handling DomainException and returning a
    custom JSON response.
    """
    response = exception_handler(exc, context)

    # Handle DomainException specifically
    if isinstance(exc, DomainException):
        return Response(
            data={"error": exc.message},
            status=status.HTTP_409_CONFLICT
        )

    return response