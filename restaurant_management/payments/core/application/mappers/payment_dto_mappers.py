from ...domain.entities.payment import Payment
from ...domain.valueobjects.payment_value_objects import *
from ...application.dtos.payment_dto import PaymentOutput 
from dataclasses import asdict
from typing import Dict, Any

class PaymentDTOMappers:
    @staticmethod
    def from_domain(payment: Payment) -> PaymentOutput:
        return PaymentOutput(
            id=payment.id,
            order_id=payment.order_id,
            payment_method=payment.payment_method.value if payment.payment_method else None,
            payment_status=payment.payment_status.value,
            sub_total=str(payment.sub_total),
            discount=str(payment.discount),
            vat_rate=str(payment.vat_rate),
            vat=str(payment.vat),
            currency_type=payment.currency_type.value,
            total=str(payment.total),
            created_at=payment.created_at.isoformat(),
            paid_at=payment.paid_at.isoformat() if payment.paid_at else None,
            items=[] # Map
        )
    
    @staticmethod
    def to_dict(paymetnDTO: PaymentOutput) -> Dict[str, Any]:
        return asdict(paymetnDTO)
    
