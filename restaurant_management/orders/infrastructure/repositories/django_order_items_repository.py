from core.exceptions.custom_exceptions import EntityNotFoundException
from ..models.order_item_model import OrderItemModel, OrderModel
from ...core.domain.entities.order_entity import Order
from ...core.mappers.order_mappers import OrderMapper, OrderItemMapper
from .django_order_repository import DjangoOrderRepository
from typing import List

# TODO: Test
class DjangoOrderItemsRepository:
    def update_order_items(self, order: Order) -> None:
        current_order_items = self._get_order_items(order.id)
        incoming_domain_items = order.order_items

        if not current_order_items:
            models_to_create = [OrderItemMapper.domain_to_model(item) for item in incoming_domain_items]
            OrderItemModel.objects.bulk_create(models_to_create)
            return

        current_item_map = {(item.menu_item_id, item.order_id): item for item in current_order_items}
        models_to_create = []
        models_to_update = []
        domain_items_to_keep = []

        for incoming_item in incoming_domain_items:
            key = (incoming_item.menu_item_id, order.id)
            if key in current_item_map:
                existing_item = current_item_map[key]
                existing_item.quantity = incoming_item.quantity
                existing_item.notes = incoming_item.notes
                existing_item.is_delivered = incoming_item.is_delivered
                models_to_update.append(existing_item)
                domain_items_to_keep.append(incoming_item.id) # Asumiendo que la entidad podría tener un id temporal (Check)
            else:
                models_to_create.append(OrderItemMapper.domain_to_model(incoming_item))

        if models_to_create:
            OrderItemModel.objects.bulk_create(models_to_create)

        if models_to_update:
            OrderItemModel.objects.bulk_update(models_to_update, ['quantity', 'notes', 'is_delivered'])

        existing_item_ids = {item.id for item in current_order_items}
        incoming_domain_item_ids = {item.id for item in incoming_domain_items if item.id is not None} # Asumiendo que los items existentes tienen ID

        items_to_delete = existing_item_ids - incoming_domain_item_ids
        if items_to_delete:
            OrderItemModel.objects.filter(id__in=items_to_delete).delete()


    def _get_order_items(self, order_id: int) -> List[OrderItemModel]:
        try:
            return OrderItemModel.objects.filter(order_id=order_id)
        except OrderModel.DoesNotExist:
            raise EntityNotFoundException('Order', order_id)

    def _get_item_by_menu_item_id(self, order_id: int, menu_item_id: int) -> OrderItemModel:
        try:
            return OrderItemModel.objects.get(menu_item_id=menu_item_id, order_id=order_id)
        except OrderItemModel.DoesNotExist:
            raise EntityNotFoundException('Order Item', f'(Order_id) {order_id} and menu_item_ID {menu_item_id}')