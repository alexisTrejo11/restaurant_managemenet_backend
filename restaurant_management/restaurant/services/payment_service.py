from restaurant.models import Payment, Order
from restaurant.services.order_service import OrderService
from datetime import datetime
from restaurant.utils.result import Result
from decimal import Decimal


class PaymentService:
    @staticmethod
    def get_payment_by_id(payment_id):
        try:
            payment = Payment.objects.get(pk=payment_id)
            return Result.success(payment)
        except Payment.DoesNotExist:
            return Result.error(f'Payment with ID {payment_id} not found')


    @staticmethod
    def get_payments_by_date_range(start_date, end_date):
        if isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date)
        if isinstance(end_date, str):
            end_date = datetime.fromisoformat(end_date)
        

        if start_date > end_date:
            return Result.error('start_date cannot be after end_date')

        payments = Payment.objects.filter(created_at_time__range=(start_date, end_date))
        return Result.success(payments)


    @staticmethod
    def get_payments_by_status(payment_status):
        return Payment.objects.filter(status=payment_status)


    @staticmethod
    def get_complete_payments_by_date_range(start_date, end_date):
        if isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date)
        if isinstance(end_date, str):
            end_date = datetime.fromisoformat(end_date)

        if start_date > end_date:
            return Result.error('start_date cannot be after end_date')

        return Payment.objects.filter(paid_at_time__range=(start_date, end_date))


    @staticmethod
    def update_payment_status(payment: Payment, payment_status: str):
        payment.status = payment_status  
        payment.save()


    @staticmethod
    def init_payment(order: Order):
        sub_total = PaymentService._calculate_payment_sub_total(order)
        discount = PaymentService._calculate_payment_discount(order)
        total = PaymentService._calculate_payment_total(sub_total, discount)

        payment = Payment(order=order, sub_total=sub_total, total=total, status='pending_payment', VAT = Payment.MEX_VAT)
        payment.save()

        return payment


    @staticmethod
    def validate_payment_creation(order: Order):
        if order.status != 'completed':
            return Result.error('order status must be completed')

        if Payment.objects.filter(order=order).exists():
            return Result.error("A payment already exists for this order")
        
        return Result.success(None)


    @staticmethod
    def complete_payment(payment: Payment):
        payment.status = 'completed'
        payment.paid_at = datetime.now()
        
        payment.save()
        
        return payment


    @staticmethod
    def _calculate_payment_sub_total(order: Order):
        items = OrderService.get_order_items(order)

        sub_total = 0
        for item in items:
            sub_total += item.menu_item.price

        return sub_total


    @staticmethod
    def _calculate_payment_discount(order: Order):
        return 0


    @staticmethod
    def _calculate_payment_total(sub_total, discount):
        total = (Decimal(sub_total) - Decimal(discount)) * (1 + Payment.MEX_VAT)
        return total
