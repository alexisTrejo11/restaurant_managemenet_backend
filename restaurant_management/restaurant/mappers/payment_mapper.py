from restaurant.services.domain.payment import Payment, PaymentItem
from restaurant.repository.models.models import PaymentItemModel, PaymentModel
from restaurant.mappers.order_mappers import OrderMappers, OrderItemMappers
from restaurant.mappers.menu_item_mappers import MenuItemMapper

class PaymentMapper:
    @staticmethod
    def to_domain(payment_model: PaymentModel) -> Payment:
        payment_items = [PaymentItemMapper.to_domain(item) for item in payment_model.payment_items.all()]

        return Payment(
            id=payment_model.id,
            order=payment_model.order if payment_model.order else None,
            payment_method=payment_model.payment_method,
            payment_status=payment_model.payment_status,
            sub_total=float(payment_model.sub_total),
            discount=float(payment_model.disccount),
            vat_rate=float(payment_model.vat_rate),
            vat=float(payment_model.vat),
            currency_type=payment_model.currency_type,
            total=float(payment_model.total),
            created_at=payment_model.created_at,
            paid_at=payment_model.paid_at,
            items=payment_items 
        )

    @staticmethod
    def to_model(payment: Payment) -> PaymentModel:
        payment_model = PaymentModel(
            id=payment.id,
            payment_method=payment.payment_method,
            payment_status=payment.payment_status,
            sub_total=payment.sub_total,
            disccount=payment.discount,
            vat_rate=payment.vat_rate,
            vat=payment.vat,
            currency_type=payment.currency_type,
            total=payment.total,
            created_at=payment.created_at,
            paid_at=payment.paid_at,
        )

        if payment.order:
            payment_model.order = OrderMappers.to_model(payment.order)

        payment_model.items = [PaymentItemMapper.to_model(item) for item in payment.items]

        return payment_model


class PaymentItemMapper:
    @staticmethod
    def to_domain(payment_item_model: PaymentItemModel) -> PaymentItem:
        return PaymentItem(
            menu_item=MenuItemMapper.to_domain(payment_item_model.menu_item) if payment_item_model.menu_item else None,
            order_item=payment_item_model.order_item,  
            price=float(payment_item_model.price),
            quantity=payment_item_model.quantity,
            total=float(payment_item_model.total),
            #extra_item_price=float(payment_item_model.extra_item_price),
            menu_extra_item=payment_item_model.menu_item_extra
        )

    @staticmethod
    def to_model(payment_item: PaymentItem) -> PaymentItemModel:
        payment_item_model = PaymentItemModel(
            menu_item=MenuItemMapper.to_model(payment_item.menu_item) if payment_item.menu_item else None,
            order_item=OrderItemMappers.to_model(payment_item.order_item),
            price=payment_item.price,
            quantity=payment_item.quantity,
            total=payment_item.total,
            menu_item_extra=payment_item.menu_extra_item
        )
        return payment_item_model
