from dataclasses import dataclass

@dataclass
class BuissnessLogicError(Exception):
    message: str
    code: str = "BUISSNESS_LOGIC_ERROR"

class ReservationDateInvalid(BuissnessLogicError):
    def __init__(self, message: str):
        super().__init__(message=message, code="RESERVATION_DATE_INVALID")

class ReservationHourInvalid(BuissnessLogicError):
    def __init__(self, message: str):
        super().__init__(message=message, code="RESERVATION_HOUR_INVALID")

class ReservationCustomerLimitExceeded(BuissnessLogicError):
    def __init__(self, message: str):
        super().__init__(message=message, code="RESERVATION_CUSTOMER_LIMIT_EXCEEDED")

class ReservationAlreadyCancelled(BuissnessLogicError):
    def __init__(self, message: str):
        super().__init__(message=message, code="RESERVATION_CUSTOMER_LIMIT_EXCEEDED")

class ReservationCannotChangeStatus(BuissnessLogicError):
    def __init__(self, message: str):
        super().__init__(message=message, code="RESERVATION_CUSTOMER_LIMIT_EXCEEDED")
