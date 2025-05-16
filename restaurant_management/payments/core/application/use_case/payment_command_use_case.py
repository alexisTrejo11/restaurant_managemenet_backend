from ..service.payment_service import PaymentService
from ..mappers.payment_mappers import PaymentMapper
from datetime import datetime

class InitPaymentUseCase:
    def __init__(self, payment_service: PaymentService):
        self.payment_service = payment_service

    def execute(self):
        pass
    
class CompletePaymentUseCase:
    def __init__(self, payment_service: PaymentService):
        self.payment_service = payment_service

    def execute(self, payment_id: int):
        pass

class CancelPaymentUseCase:
    def __init__(self, payment_service: PaymentService):
        self.payment_service = payment_service

    def execute(self):
        pass

class UpdateStatusUseCase:
    def __init__(self, payment_service: PaymentService):
        self.payment_service = payment_service

    def execute(self):
        pass

    