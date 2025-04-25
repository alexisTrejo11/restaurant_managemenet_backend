from ..models.order_item_model import OrderItemModel, OrderModel
from ...core.domain.entities.order_entity import Order
from ...core.mappers.order_mappers import OrderMapper, OrderItemMapper

class DjangoOrderItemsRepository:
    def update_order_items(self, order: Order) -> Order:
        """
        Update the items associated with an order.
        
        Args:
            order (Order): The order entity containing updated items.
        
        Returns:
            Order: The updated order.
        """
        order_model = OrderModel.objects.filter(id=order.id).first()
        if not order_model:
            raise ValueError(f"Order with id {order.id} not found")

        self.__delete_items(order)

        for item in order.items:
            item_model = OrderItemMapper.to_model(item)
            item_model.order = order_model

            if item.id:
                self.__update_items(item, item_model)
            else:
                item_model.save()

        return OrderMapper.to_domain(order_model)

    def delete_items(self, order: Order):
        """
        Delete items that are no longer associated with an order.
        
        Args:
            order (Order): The order entity containing updated items.
        """
        existing_items = OrderItemModel.objects.filter(order=order.id)
        existing_item_ids = {item.id for item in existing_items}
        current_item_ids = {item.id for item in order.items if item.id}

        items_to_delete = existing_item_ids - current_item_ids
        if items_to_delete:
            OrderItemModel.objects.filter(id__in=items_to_delete).delete()

    def __update_items(self, item, item_model):
        """
        Update an existing order item in the database.
        
        Args:
            item: The updated order item entity.
            item_model: The corresponding database model.
        """
        existing_item = OrderItemModel.objects.filter(id=item.id).first()
        for field, value in item_model.__dict__.items():
            if field != 'id' and not field.startswith('_'):
                setattr(existing_item, field, value)

        existing_item.save()