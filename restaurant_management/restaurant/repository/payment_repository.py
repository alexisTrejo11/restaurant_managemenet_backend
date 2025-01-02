from abc import ABC
from typing import Optional, List
from restaurant.repository.models.models import PaymentModel, PaymentItemModel
from restaurant.services.domain.payment import Payment  
from restaurant.mappers.payment_mapper import PaymentMapper, PaymentItemMapper
from restaurant.repository.common_repository import CommonRepository
from django.db.models import ObjectDoesNotExist
from django.utils.timezone import now


class PaymentRepository(CommonRepository[Payment], ABC):
    def create(self, payment: Payment) -> Payment:
        payment_model = PaymentMapper.to_model(payment)
        
        payment_model.created_at = now()
        payment_model.save()
        
        return PaymentMapper.to_domain(payment_model)


    def get_by_id(self, id: int) -> Optional[Payment]:
            payment_model = PaymentModel.objects.filter(id=id).first()
            
            if payment_model:
                return PaymentMapper.to_domain(payment_model)
            
            
    def get_by_date_range(self, start_date, end_date):
        payment_models = PaymentModel.objects.filter(created_at__range=(start_date, end_date))
        
        return [PaymentMapper.to_domain(payment_model) for payment_model in payment_models]


    def get_complete_payments_by_date_range(self, start_date, end_date):
        payment_models = PaymentModel.objects.filter(paid_at__range=(start_date, end_date))
        return [PaymentMapper.to_domain(payment_model) for payment_model in payment_models]


    def get_all(self) -> List[Payment]:
        payment_models = PaymentModel.objects.all()
        
        return [PaymentMapper.to_domain(payment_model) for payment_model in payment_models]


    def get_by_status(self, payment_status):
        payment_models = PaymentModel.objects.filter(payment_status=payment_status)
        
        return [PaymentMapper.to_domain(payment_model) for payment_model in payment_models]


    def update(self, entity: Payment) -> Payment:
        try:
            payment_model = PaymentModel.objects.get(id=entity.id)
            payment_model.payment_method = entity.payment_method
            payment_model.payment_status = entity.payment_status
            payment_model.sub_total = entity.sub_total
            payment_model.disccount = entity.discount
            payment_model.vat_rate = entity.vat_rate
            payment_model.vat = entity.vat
            payment_model.currency_type = entity.currency_type
            payment_model.total = entity.total
            payment_model.paid_at = entity.paid_at
            payment_model.save()
            return PaymentMapper.to_domain(payment_model)
        except ObjectDoesNotExist:
            raise ValueError(f"Payment with ID {entity.order_id} does not exist.")


    def delete(self, id: int) -> bool:
        deleted, _ = PaymentModel.objects.filter(id=id).delete()
        return deleted > 0

    
    def save_payment_items(self, payment, payment_items):
        saved_items = []

        for item in payment_items:
            payment_item_model = PaymentItemMapper.to_model(item)
            payment_item_model.payment = PaymentMapper.to_model(payment)
            payment_item_model.save()
            
            saved_items.append(PaymentItemMapper.to_domain(payment_item_model))
        
        return saved_items
            

