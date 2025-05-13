from dataclasses import dataclass

@dataclass
class DomainError(Exception):
    message: str
    code: str = "DOMAIN_ERROR"


class ReservationDateInvalid(DomainError):
    def __init__(self, message: str):
        super().__init__(message=message, code="RESERVATION_DATE_INVALID")


class ReservationHourInvalid(DomainError):
    def __init__(self, message: str):
        super().__init__(message=message, code="RESERVATION_HOUR_INVALID")


class ReservationCustomerLimitExceeded(DomainError):
    def __init__(self, message: str):
        super().__init__(message=message, code="RESERVATION_CUSTOMER_LIMIT_EXCEEDED")