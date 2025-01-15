from ast import Return
from datetime import datetime
from typing import Optional
from decimal import Decimal
from restaurant.services.domain.order import Order
from restaurant.utils.result import Result
from restaurant.utils.exceptions import DomainException
from restaurant.services.domain.menu_item import MenuItem
from restaurant.services.domain.order import OrderItem
from restaurant.services.domain.menu_extra import MenuExtraDomain

class PaymentItem:
    def __init__(
            self,
            menu_item : MenuItem, 
            order_item : OrderItem,
            price,
            quantity, 
            total = 0,
            extra_item_price = 0, 
            menu_extra_item : MenuExtraDomain = None, 
        ):
        self.menu_item = menu_item
        self.menu_extra_item = menu_extra_item
        self.order_item = order_item
        self.price = price
        self.quantity = quantity
        self.total = total
        self.extra_item_price = extra_item_price
    
    def increase_menu_extra(self):
        self.total += Decimal(self.extra_item_price)

    def increase_item_quantity(self, quantity):
        self.quantity += quantity

    def calculate_total(self):
        self.total = Decimal(self.quantity) * Decimal(self.price)


class Payment:
    def __init__(
        self,
        order,
        payment_status: str,
        sub_total: Decimal,
        discount: Decimal,
        currency_type: str,
        total: Decimal,
        vat: Decimal,
        vat_rate: Decimal = None,
        id = None,
        payment_method: str = None,
        created_at: Optional[datetime] = None,
        paid_at: Optional[datetime] = None,
        items=None
    ):
        self.id = id
        self.order = order
        self.payment_method = payment_method
        self.payment_status = payment_status
        self.sub_total = sub_total
        self.discount = discount
        self.vat_rate = vat_rate
        self.vat = vat
        self.currency_type = currency_type
        self.total = total
        self.created_at = created_at
        self.paid_at = paid_at
        self.items = items if items is not None else []

    MEX_VAT = Decimal('0.16') 

    @staticmethod
    def init_payment(order: Order):
        return Payment(
            order=order,
            sub_total=Decimal('0.00'),
            total=Decimal('0.00'),
            payment_status='pending_payment',
            vat=Decimal('0.00'),
            vat_rate=Payment.MEX_VAT,
            discount=Decimal('0.00'),
            currency_type='MXN',
            items=[]
        )


    def calculate_numbers(self):
        self.sub_total = self.__calculate_sub_total()
        self.discount = self.__calculate_discount()
        self.vat = self.__calculate_taxes(self.sub_total, self.discount)
        self.total = self.__calculate_total(self.sub_total, self.discount, self.vat)


    def validate_payment_complete(self):
        if not self.__is_status_pending():
           return Result.error("only pending payments can be completed")

        return Result.success()

    def validate_payment_cancel(self):
        if not self.__is_status_pending():
           return Result.error("only pending payments can be cancel")

        return Result.success()
    
    def validate_payment_method(self, payment_method):
        valid_payment_methods = ['CARD', 'CASH']
        if not payment_method in valid_payment_methods:
           return Result.error("invalid payment method")

        return Result.success()
    
    def __is_status_pending(self): 
        return self.payment_status == 'PENDING_PAYMENT'


    @staticmethod
    def validate_pending_status(status: str):
        if status in ['CANCELLED', 'COMPLETE']:
            raise ValueError("Payment already processed")


    def validate_payment_status(self, status: str):
        valid_statuses = ['PENDING_PAYMENT', 'COMPLETE', 'CANCELLED']
        if status not in valid_statuses:
            raise DomainException(f"Invalid payment status: {status}")


    def complete_payment(self, payment_method):
        self.set_as_complete()
        self.payment_method = payment_method
        self.paid_at = datetime.now()


    def set_as_complete(self):
        self.payment_status = 'COMPLETED'


    def __calculate_sub_total(self):
        items = self.items 
        item_total = sum(Decimal(item.total) for item in items)
        return item_total


    def __calculate_discount(self):
        return Decimal('0.00')


    def __calculate_taxes(self, sub_total: Decimal, discount: Decimal):
        amount_pre_tax = Decimal(sub_total) - Decimal(discount)
        return amount_pre_tax * self.vat_rate


    def __calculate_total(self, sub_total: Decimal, discount: Decimal, taxes: Decimal):
        return (Decimal(sub_total) - Decimal(discount)) + taxes


    def __str__(self):
        return f"Payment(order_id={self.order_id}, total={self.total}, currency={self.currency_type})"
