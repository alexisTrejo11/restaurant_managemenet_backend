from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from ..valueobjects.payment_value_objects import PaymentMethod, PaymentStatus, CurrencyType
from .payment_item import PaymentItem

@dataclass
class Payment:
    id: Optional[int] = None
    order_id: Optional[int] = None
    payment_method: Optional[PaymentMethod] = None
    payment_status: PaymentStatus = PaymentStatus.PENDING
    sub_total: Decimal = Decimal('0.00')
    discount: Decimal = Decimal('0.00')
    vat_rate: Decimal = Decimal('0.00')
    vat: Decimal = Decimal('0.00')
    currency_type: CurrencyType = CurrencyType.MXN
    total: Decimal = Decimal('0.00')
    created_at: datetime = datetime.now()
    paid_at: Optional[datetime] = None
    items: List[PaymentItem] = None

    def __post_init__(self):
        if self.items is None:
            self.items = []
        
        if self.sub_total == Decimal('0.00'):
            self.sub_total = sum(item.total for item in self.items)
        
        if self.vat == Decimal('0.00') and self.vat_rate > Decimal('0.00'):
            self.vat = (self.sub_total - self.discount) * (self.vat_rate / Decimal('100'))
        
        if self.total == Decimal('0.00'):
            self.total = self.sub_total - self.discount + self.vat
    
    @staticmethod
    def validate_method(status: str):
        if not status in PaymentMethod.get_methods():
            raise ValueError("Invalid Payment Status")
    
    @staticmethod
    def validate_status(status: str):
        if not status in PaymentStatus.get_all_staus():
            raise ValueError("Invalid Payment Status")
    
    def complete(self):
        if self.payment_status == PaymentStatus.CANCELLED:
            raise ValueError("Cannot complete a cancelled payment")
        self.payment_status = PaymentStatus.COMPLETED
        self.paid_at = datetime.now()

    def cancel(self):
        if self.payment_status == PaymentStatus.COMPLETED:
            raise ValueError("Cannot cancel a completed payment")
        self.payment_status = PaymentStatus.CANCELLED 

    def add_items(self, items: List[PaymentItem]):
        self.items.append(items)
        self.calculate_numbers()

    def calculate_numbers(self):
        self.sub_total = self.__calculate_sub_total()
        self.discount = self.__calculate_discount()
        self.vat = self.__calculate_taxes(self.sub_total, self.discount)
        self.total = self.__calculate_total(self.sub_total, self.discount, self.vat)

    def __calculate_sub_total(self):
        return sum(Decimal(item.total) for item in self.items)

    def __calculate_discount(self):
        return Decimal('0.00')

    def __calculate_taxes(self, sub_total: Decimal, discount: Decimal):
        amount_pre_tax = Decimal(sub_total) - Decimal(discount)
        return amount_pre_tax * self.vat_rate

    def __calculate_total(self, sub_total: Decimal, discount: Decimal, taxes: Decimal):
        return (Decimal(sub_total) - Decimal(discount)) + taxes