from dataclasses import dataclass
from typing import Optional
from decimal import Decimal

@dataclass
class PaymentItem:
    menu_item_id: int
    menu_item_name: str
    menu_item_extra_id: Optional[int]
    menu_item_extra_name: Optional[str]
    price: Decimal
    quantity: int
    extras_charges: Decimal = Decimal('0.00')
    total: Decimal = Decimal('0.00')

    def __post_init__(self):
        self.total = self.price * Decimal(self.quantity) + self.extras_charges