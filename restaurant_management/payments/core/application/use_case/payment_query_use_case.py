from ..service.payment_service import PaymentService
from ..mappers.payment_mappers import PaymentMapper
from datetime import datetime

class GetPaymentByIdUseCase:
    def __init__(self, payment_service: PaymentService):
        self.payment_service = payment_service

    def execute(self, payment_id: int):
        payment = self.payment_service.get_payment_by_id(payment_id)
        return PaymentMapper.to_DTO(payment)
    

#TODO:Implement
class GetPaymentByOrderUseCase:
    def __init__(self, payment_service: PaymentService):
        self.payment_service = payment_service

    def execute(self, payment_id: int):
        payment = self.payment_service.get_payment_by_id(payment_id)
        return PaymentMapper.to_DTO(payment)

class ListByDateRangeUseCase:
    def __init__(self, payment_service: PaymentService):
        self.payment_service = payment_service

    def execute(self, start_date: datetime, end_date: datetime, only_completed=False):
        payment_list = self.payment_service.get_payments_by_date_range(start_date ,end_date, only_completed)
        return [PaymentMapper.to_DTO(payment) for payment in payment_list]
    

class ListByStatusUseCase:
    def __init__(self, payment_service: PaymentService):
        self.payment_service = payment_service

    def execute(self, status: str):
        payment_list = self.payment_service.get_payments_by_status(status)
        return [PaymentMapper.to_DTO(payment) for payment in payment_list]
    
