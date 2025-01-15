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
            menu_item: MenuItem, 
            order_item: OrderItem,
            price: Decimal,
            quantity: int, 
            total: Decimal = Decimal('0.00'),
            extra_item_price: Decimal = Decimal('0.00'), 
            menu_extra_item: Optional[MenuExtraDomain] = None, 
        ):
        self.__menu_item = menu_item
        self.__menu_extra_item = menu_extra_item
        self.__order_item = order_item
        self.__price = price
        self.__quantity = quantity
        self.__total = total
        self.__extra_item_price = extra_item_price
    
    @property
    def menu_item(self):
        return self.__menu_item

    @property
    def menu_extra_item(self):
        return self.__menu_extra_item

    @property
    def order_item(self):
        return self.__order_item

    @property
    def price(self):
        return self.__price

    @property
    def quantity(self):
        return self.__quantity

    @property
    def total(self):
        return self.__total

    @property
    def extra_item_price(self):
        return self.__extra_item_price

    def increase_menu_extra(self):
        self.__total += self.__extra_item_price

    def increase_item_quantity(self, quantity: int):
        self.__quantity += quantity

    def calculate_total(self):
        self.__total = Decimal(self.__quantity) * Decimal(self.__price)


class Payment:
    MEX_VAT = Decimal('0.16') 

    def __init__(
        self,
        order: Order,
        payment_status: str,
        sub_total: Decimal,
        discount: Decimal,
        currency_type: str,
        total: Decimal,
        vat: Decimal,
        vat_rate: Decimal = None,
        id: Optional[int] = None,
        payment_method: Optional[str] = None,
        created_at: Optional[datetime] = None,
        paid_at: Optional[datetime] = None,
        items: Optional[list] = None
    ):
        self.__id = id
        self.__order = order
        self.__payment_method = payment_method
        self.__payment_status = payment_status
        self.__sub_total = sub_total
        self.__discount = discount
        self.__vat_rate = vat_rate or Payment.MEX_VAT
        self.__vat = vat
        self.__currency_type = currency_type
        self.__total = total
        self.__created_at = created_at
        self.__paid_at = paid_at
        self.__items = items or []

    @property
    def id(self):
        return self.__id

    @property
    def order(self):
        return self.__order

    @property
    def payment_method(self):
        return self.__payment_method

    @payment_method.setter
    def payment_method(self, value: Optional[str]):
        self.__payment_method = value

    @property
    def payment_status(self):
        return self.__payment_status

    @payment_status.setter
    def payment_status(self, value: str):
        self.__payment_status = value

    @property
    def sub_total(self):
        return self.__sub_total

    @property
    def discount(self):
        return self.__discount

    @property
    def vat_rate(self):
        return self.__vat_rate

    @property
    def vat(self):
        return self.__vat

    @property
    def currency_type(self):
        return self.__currency_type

    @property
    def total(self):
        return self.__total

    @property
    def created_at(self):
        return self.__created_at

    @property
    def paid_at(self):
        return self.__paid_at

    @property
    def items(self):
        return self.__items

    def __str__(self):
        return f"Payment(order_id={self.__order.id}, total={self.__total}, currency={self.__currency_type})"

    @staticmethod
    def init_payment(order: Order):
        return Payment(
            order=order,
            sub_total=Decimal('0.00'),
            total=Decimal('0.00'),
            payment_status='PENDING_PAYMENT',
            vat=Decimal('0.00'),
            vat_rate=Payment.MEX_VAT,
            discount=Decimal('0.00'),
            currency_type='MXN',
            items=[]
        )

    def calculate_numbers(self):
        self.__sub_total = self.__calculate_sub_total()
        self.__discount = self.__calculate_discount()
        self.__vat = self.__calculate_taxes(self.__sub_total, self.__discount)
        self.__total = self.__calculate_total(self.__sub_total, self.__discount, self.__vat)

    def validate_payment_complete(self):
        if not self.__is_status_pending():
            return Result.error("Only pending payments can be completed")
        return Result.success()

    def validate_payment_cancel(self):
        if not self.__is_status_pending():
            return Result.error("Only pending payments can be cancel")
        return Result.success()

    def validate_payment_method(self, payment_method: str):
        valid_payment_methods = ['CARD', 'CASH']
        if payment_method not in valid_payment_methods:
            return Result.error("Invalid payment method")
        return Result.success()

    def __is_status_pending(self): 
        return self.__payment_status == 'PENDING_PAYMENT'

    @staticmethod
    def validate_pending_status(status: str):
        if status in ['CANCELLED', 'COMPLETE']:
            raise ValueError("Payment already processed.")

    def validate_payment_status(self, status: str):
        valid_statuses = ['PENDING_PAYMENT', 'COMPLETE', 'CANCELLED']
        if status not in valid_statuses:
            raise DomainException(f"Invalid payment status: {status}")

    def complete_payment(self, payment_method: str):
        self.set_as_complete()
        self.__payment_method = payment_method
        self.__paid_at = datetime.now()

    def set_as_complete(self):
        self.__payment_status = 'COMPLETED'

    def __calculate_sub_total(self):
        return sum(Decimal(item.total) for item in self.__items)

    def __calculate_discount(self):
        return Decimal('0.00')

    def __calculate_taxes(self, sub_total: Decimal, discount: Decimal):
        amount_pre_tax = Decimal(sub_total) - Decimal(discount)
        return amount_pre_tax * self.__vat_rate

    def __calculate_total(self, sub_total: Decimal, discount: Decimal, taxes: Decimal):
        return (Decimal(sub_total) - Decimal(discount)) + taxes
