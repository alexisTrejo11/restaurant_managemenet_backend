from datetime import datetime
from decimal import Decimal
from typing import Optional
from ...domain.valueobjects import Payment, PaymentMethod, PaymentStatus, CurrencyType
from ...infrastructure.persistence.models.payment_model import PaymentModel

class PaymentModelMapper:
    @staticmethod
    def from_domain(payment: Payment) -> PaymentModel:
        """
        Converts a domain Payment entity to a Django PaymentModel.

        Args:
            payment: Domain Payment entity.

        Returns:
            PaymentModel instance ready to save to the database.
        """
        return PaymentModel(
            id=payment.id,
            order_id=payment.order_id,
            payment_method=payment.payment_method.value if payment.payment_method else None,
            payment_status=payment.payment_status.value,
            sub_total=payment.sub_total,
            discount=payment.discount,
            vat_rate=payment.vat_rate,
            vat=payment.vat,
            currency_type=payment.currency_type.value,
            total=payment.total,
            created_at=payment.created_at,
            paid_at=payment.paid_at
        )

    @staticmethod
    def to_domain(payment_model: PaymentModel) -> Payment:
        """
        Converts a Django PaymentModel to a domain Payment entity.

        Args:
            payment_model: Django PaymentModel instance.

        Returns:
            Domain Payment entity with all fields mapped.
        """
        return Payment(
            id=payment_model.id,
            order_id=payment_model.order.id if payment_model.order else None,
            payment_method=PaymentMethod(payment_model.payment_method) if payment_model.payment_method else None,
            payment_status=PaymentStatus(payment_model.payment_status),
            sub_total=payment_model.sub_total,
            discount=payment_model.discount,
            vat_rate=payment_model.vat_rate,
            vat=payment_model.vat,
            currency_type=CurrencyType(payment_model.currency_type),
            total=payment_model.total,
            created_at=payment_model.created_at,
            paid_at=payment_model.paid_at,
            items=[]  # Items need to be mapped separately with PaymentItemModelMapper
        )