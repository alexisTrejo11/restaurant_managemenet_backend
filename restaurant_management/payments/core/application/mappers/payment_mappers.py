from ...domain.entities.payment import Payment
from ...application.dtos.payment_dto import PaymentOutput 
from dataclasses import asdict
from typing import Dict, Any
from decimal import Decimal
from ...domain.valueobjects.payment_value_objects import *
from orders.core.domain.entities.order_entity import Order

class PaymentMapper:
    @staticmethod
    def from_dict(payment_dict: Dict[str, Any]) -> Payment:
        """
        Converts a dictionary to a domain Payment entity.

        Args:
            payment_dict: Dictionary with the payment data.

        Returns:
            Instance of Payment with the validated data.
        """
        items_dict = payment_dict.pop('items', [])

        if 'payment_method' in payment_dict and payment_dict['payment_method']:
            payment_dict['payment_method'] = PaymentMethod(payment_dict['payment_method'])

        if 'payment_status' in payment_dict:
            payment_dict['payment_status'] = PaymentStatus(payment_dict['payment_status'])

        if 'currency_type' in payment_dict:
            payment_dict['currency_type'] = CurrencyType(payment_dict['currency_type'])

        for date_field in ['created_at', 'paid_at']:
            if date_field in payment_dict and payment_dict[date_field]:
                if isinstance(payment_dict[date_field], str):
                    payment_dict[date_field] = datetime.fromisoformat(payment_dict[date_field])

        for decimal_field in ['sub_total', 'discount', 'vat_rate', 'vat', 'total']:
            if decimal_field in payment_dict and payment_dict[decimal_field]:
                if isinstance(payment_dict[decimal_field], str):
                    payment_dict[decimal_field] = Decimal(payment_dict[decimal_field])

        return Payment(
            **payment_dict,
            items=[]
        )

    @staticmethod
    def to_DTO(payment: Payment) -> PaymentOutput:
        """
        Converts a Payment entity to an output DTO.

        Args:
            payment: Payment instance to convert.

        Returns:
            PaymentOutput ready to be serialized to JSON.
        """
        payment_data = asdict(payment)

        for enum_field in ['payment_method', 'payment_status', 'currency_type']:
            if payment_data.get(enum_field):
                payment_data[enum_field] = payment_data[enum_field].value

        for date_field in ['created_at', 'paid_at']:
            if payment_data.get(date_field):
                payment_data[date_field] = payment_data[date_field].isoformat()

        for decimal_field in ['sub_total', 'discount', 'vat_rate', 'vat', 'total']:
            if payment_data.get(decimal_field) is not None:
                payment_data[decimal_field] = str(payment_data[decimal_field])

        payment_items = []
        for item in payment.items:
            item_data = asdict(item)
            for decimal_field in ['price', 'extras_charges', 'total']:
                if item_data.get(decimal_field) is not None:
                    item_data[decimal_field] = str(item_data[decimal_field])
            payment_items.append(item_data)

        payment_data['items'] = payment_items

        return PaymentOutput(**payment_data)
    

    def init_from_order(order: Order) -> Payment:
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
    