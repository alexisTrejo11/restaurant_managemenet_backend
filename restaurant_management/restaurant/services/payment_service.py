from datetime import datetime
from typing import List, Optional
from restaurant.repository.payment_repository import PaymentRepository 
from restaurant.services.domain.payment import Payment, PaymentItem
from restaurant.services.domain.order import OrderItem
from restaurant.services.domain.payment import Payment
from restaurant.services.domain.order import Order
from restaurant.utils.result import Result
from injector import inject
import logging

logger = logging.getLogger(__name__)

class PaymentService:
    @inject
    def __init__(self, payment_repository : PaymentRepository):
        self.payment_repository = payment_repository

    def get_payment_by_id(self, payment_id) -> Optional[Payment]:
            return self.payment_repository.get_by_id(payment_id)

    def valdiate_payment_status(self, status):
        valid_statuses = ['pending_payment', 'completed', 'cancelled']
        return status in valid_statuses       


    def get_payments_by_date_range(self, start_date, end_date):
        if isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date)
        if isinstance(end_date, str):
            end_date = datetime.fromisoformat(end_date)

        if start_date > end_date:
           raise ValueError('start_date cannot be after end_date')

        return self.payment_repository.get_by_date_range(start_date, end_date)


    def get_payments_by_status(self, payment_status):
        return self.payment_repository.get_by_status(payment_status)


    def get_complete_payments_by_date_range(self, start_date, end_date):
        if start_date > end_date:
            raise ValueError('start_date cannot be after end_date')

        return self.payment_repository.get_complete_payments_by_date_range(start_date, end_date)


    def create_payment(self, order: Order):
        payment = self._initialize_payment(order)
        self._validate_payment(payment, order)

        payment_items = self._generate_payment_items(order.items)
        payment = self._calculate_payment(payment, payment_items)

        payment_created = self._save_payment_and_items(payment, payment_items)
        logger.info(f"Payment created for order with ID {order.id}.")

        return payment_created


    def complete_payment(self, payment: Payment, payment_method: str) -> Result:
        method_validation = payment.validate_payment_method(payment_method)
        if method_validation.is_failure():
            logger.warning(f"Payment method validation failed for payment ID {payment.id} using method {payment_method}.")
            return method_validation

        payment.complete_payment(payment_method)
        
        completed_payment = self.payment_repository.update(payment)
        logger.info(f"Payment with ID {payment.id} completed using method {payment_method}.")

        return Result.success(completed_payment)


    def update_payment_status(self, payment: Payment, status: str):
        payment.validate_payment_status(status)
        payment.payment_status = status
        
        self.payment_repository.update(payment)
        logger.info(f"Payment status for payment ID {payment.id} updated to {status}.")


    def validate_payment_complete(self, payment: Payment) -> Result:
        return payment.validate_payment_complete()
    

    def validate_payment_cancel(self, payment: Payment) -> Result:
        return payment.validate_payment_cancel()
    
    
    def generate_payment_items(self, order_items: List[OrderItem]) -> List[PaymentItem]:
        payment_items = {}

        for order_item in order_items:
            key = (
                order_item.menu_item.id, 
                order_item.menu_extra.id if order_item.menu_extra else None
            )

            if key in payment_items:
                payment_items[key].increase_item_quantity(order_item.quantity)
                payment_items[key].calculate_total()
            else:
                payment_items[key] = self.__create_payment_item(order_item)

        return list(payment_items.values())
        
        
    def __create_payment_item(self, order_item : OrderItem):
        payment_item = PaymentItem(
                menu_item=order_item.menu_item,
                menu_extra_item=order_item.menu_extra,
                order_item=order_item,
                quantity=order_item.quantity,
                price=order_item.menu_item.price
            )

        payment_item.calculate_total()

        if payment_item.menu_extra_item:
            payment_item.menu_extra_item = order_item.menu_extra.price
            payment_item.increase_extra_item_price()
        
        return payment_item


    def _save_payment_and_items(self, payment: Payment, payment_items):
        payment_created = self.payment_repository.create(payment)
        payment_items_created = self.payment_repository.save_payment_items(payment_created, payment_items)
        payment_created.items = payment_items_created
        return payment_created

    def _initialize_payment(self, order: Order):
            return Payment.init_payment(order)

    def _validate_payment(self, payment: Payment, order: Order):
        payment.validate_payment_creation(order)

    def _generate_payment_items(self, order_items):
        return self.generate_payment_items(order_items)

    def _calculate_payment(self, payment: Payment, payment_items):
        payment.items = payment_items
        payment.calculate_numbers()
        return payment

    def _save_payment_and_items(self, payment: Payment, payment_items):
        payment_created = self.payment_repository.create(payment)
        payment_items_created = self.payment_repository.save_payment_items(payment_created, payment_items)
        payment_created.items = payment_items_created
        return payment_created
