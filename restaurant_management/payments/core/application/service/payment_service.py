from datetime import datetime
from typing import List, Optional
from restaurant.repository.payment_repository import PaymentRepository 
from restaurant.services.domain.payment import Payment, PaymentItem
from restaurant.services.domain.order import OrderItem
from ...domain.entities.payment import Payment
from restaurant.services.domain.order import Order
from injector import inject
from decimal import Decimal
from ..mappers.payment_mappers import PaymentMapper 

class PaymentService:
    @inject
    def __init__(self, payment_repository : PaymentRepository):
        self.payment_repository = payment_repository

    def get_payment_by_id(self, payment_id: int) -> Optional[Payment]:
            return self.payment_repository.get_by_id(payment_id)

    def get_payments_by_date_range(self, start_date: datetime, end_date: datetime, only_completed=False):
        if start_date > end_date:
           raise ValueError('start_date cannot be after end_date')

        return self.payment_repository.get_by_date_range(start_date, end_date)

    def get_payments_by_status(self, payment_status: str) -> List[Payment]:        
        payment_status = payment_status.strip().upper()
        
        Payment.validate_status(payment_status)

        return self.payment_repository.get_by_status(payment_status)


    def create_payment(self, order: Order):
        payment = PaymentMapper.init_from_order(order)

        payment_items = self.generate_payment_items(order.items)
        payment.add_items(payment_items)

        payment_created = self.payment_repository.create(payment)

        return self.__save_payment_items(payment_created, payment_items)

    def complete_payment(self, payment: Payment, payment_method: str) -> Payment:
        Payment.validate_status(payment_method)
        
        payment.complete(payment_method)
        
        completed_payment = self.payment_repository.update(payment)

        return completed_payment


    def update_payment_status(self, payment: Payment, status: str):
        payment.validate_payment_status(status)
        payment.payment_status = status
        
        self.payment_repository.update(payment)
    
    def cancel(self, payment: Payment) -> None:
        payment.cancel()
        self.payment_repository.update(payment)

        
    def __create_payment_item(self, order_item : OrderItem):
        payment_item = PaymentItem(
                menu_item=order_item.menu_item,
                menu_extra_item=order_item.menu_extra,
                order_item=order_item,
                quantity=order_item.quantity,
                price=Decimal(order_item.menu_item.price)
            )

        payment_item.calculate_total()

        if payment_item.menu_extra_item:
            payment_item.extra_item_price = Decimal(order_item.menu_extra.price) 
            payment_item.menu_extra_item = order_item.menu_extra
            payment_item.increase_menu_extra()

        return payment_item

    def __save_payment_items(self, payment: Payment, payment_items):
        payment_items_created = self.payment_repository.save_payment_items(payment, payment_items)
        payment.items = payment_items_created
        return payment

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
