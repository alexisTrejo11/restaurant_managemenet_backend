from dataclasses import dataclass
from typing import List, Optional
from .payment_item_dto import PaymentItemOutput

@dataclass
class PaymentOutput:
    id: int
    order_id: int
    payment_method: str
    payment_status: str
    sub_total: str
    discount: str
    vat_rate: str
    vat: str
    currency_type: str
    total: str
    created_at: str
    paid_at: Optional[str]
    items: List[PaymentItemOutput]