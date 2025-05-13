from dataclasses import dataclass
from typing import Optional

@dataclass
class PaymentItemOutput:
    menu_item_id: int
    menu_item_name: str
    menu_item_extra_id: Optional[int]
    menu_item_extra_name: Optional[str]
    price: str
    quantity: int
    extras_charges: str
    total: str
