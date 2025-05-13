from ....application.repositories.payment_repository import PaymentRepository
from ...persistence.models.payment_model import PaymentModel
from ....domain.entities.payment import Payment
from ....infrastructure.mappers.pay_model_mappers import PaymentModelMapper
from typing import Optional
from core.exceptions.custom_exceptions import EntityNotFoundException


class DjangoPaymentRepository(PaymentRepository):
    # TODO: PAGINATE
    def get_all(self) -> list:
        payment_query_set = PaymentModel.objects.get_queryset()
        return [PaymentModelMapper.to_domain(payment) for payment in payment_query_set]

    def get_by_id(self, id: int, raise_exception=False) -> Optional[Payment]:
        try:
            payment = PaymentModel.objects.get(id=id)
            PaymentModelMapper.to_domain(payment)
        except PaymentModel.DoesNotExist:
            if raise_exception:
                raise EntityNotFoundException("Paymnet", id)
            else:
                return None
            
    def get_by_order_id(self, order_id: int) -> Optional[Payment]:
        payment = PaymentModel.objects.filter(order_id=order_id).first()
        if payment:
            PaymentModelMapper.to_domain(payment)

    def save(self, payment: Payment) -> Payment:
        payment_model = PaymentModelMapper.from_domain(payment)

        if not payment.id:
            return self._create(payment_model)
        else:
            return self._update(payment_model)            


    def delete(self, id: int):
        PaymentModel.objects.delete(id)

    def _create(self, payment: PaymentModel) -> Payment:
        payment_created = PaymentModel.objects.create(payment)
        return PaymentModelMapper.to_domain(payment_created)

    def _update(self, payment: PaymentModel) -> Payment:
        payment_updated = PaymentModel.objects.update(payment)
        return PaymentModelMapper.to_domain(payment_updated)


