class CustomException(Exception):
    """
    Base class for all custom exceptions.
    """
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class EntityNotFoundException(CustomException):
    """
    Exception raised when an entity is not found in the database.
    """
    def __init__(self, entity_name: str, entity_id: int):
        message = f"{entity_name} with ID {entity_id} not found."
        super().__init__(message=message, status_code=404)


class InvalidFilterException(CustomException):
    """
    Exception raised when filter parameters are invalid.
    """
    def __init__(self, filter_name: str):
        message = f"Invalid filter: {filter_name}."
        super().__init__(message=message, status_code=400)


class BusinessRuleViolationException(CustomException):
    """
    Exception raised when a business rule is violated.
    """
    def __init__(self, rule_description: str):
        message = f"Business rule violation: {rule_description}."
        super().__init__(message=message, status_code=409)


class DomainException(CustomException):
    """
    Exception raised when a domain rule is violated.
    """
    def __init__(self, rule_description: str):
        message = f"Domain rule violation: {rule_description}."
        super().__init__(message=message, status_code=409)