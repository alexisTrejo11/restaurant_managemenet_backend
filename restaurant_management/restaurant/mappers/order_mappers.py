from restaurant.models import OrderModel, OrderItemModel, TableModel, MenuItemModel
from restaurant.services.domain.order import Order, OrderItem
from restaurant.serializers import OrderSerializer
from restaurant.mappers.table_mappers import TableMappers
from restaurant.mappers.menu_item_mappers import MenuItemMapper
from restaurant.mappers.menu_extra_mappers import MenuExtraMapper

class OrderMappers:
    @staticmethod
    def to_model(order: Order) -> OrderModel:
        order_model = OrderModel(
            id=order.id,
            table=TableMappers.to_model(order.table), 
            status=order.status,
            created_at=order.created_at,
            end_at=order.end_at,
        )
        return order_model

    @staticmethod
    def to_domain(order_model: OrderModel):
        items = [OrderItemMappers.to_domain(item) for item in order_model.order_items.all()]
        return Order(
            id=order_model.id,
            table=TableMappers.to_domain(order_model.table),
            status=order_model.status,
            created_at=order_model.created_at,
            end_at=order_model.end_at,
            items=items, 
        )


    @staticmethod
    def serializer_to_domain(order_serializer: OrderSerializer):
        return Order(
            status=order_serializer.validated_data['status'],
            created_at=order_serializer.validated_data['created_at'],
            end_at=order_serializer.validated_data.get('end_at'),
        )

class OrderItemMappers:
    @staticmethod
    def to_model(order_item: OrderItem):
        menu_extra = MenuExtraMapper.to_model(order_item.menu_extra) if order_item.menu_extra else None

        order_item_model = OrderItemModel(
            id=order_item.id,
            menu_item=MenuItemMapper.to_model(order_item.menu_item),
            menu_extra=menu_extra,
            is_delivered=order_item.is_delivered,
            notes=order_item.notes,
            quantity=order_item.quantity,
            added_at=order_item.added_at,
        )
        return order_item_model


    @staticmethod
    def to_domain(order_item_model: OrderItemModel) -> OrderItem:
        menu_extra = MenuExtraMapper.to_domain(order_item_model.menu_extra) if order_item_model.menu_extra else None

        return OrderItem(
            id=order_item_model.id,
            menu_item=MenuItemMapper.to_domain(order_item_model.menu_item),
            menu_extra=menu_extra,
            quantity=order_item_model.quantity,
            notes=order_item_model.notes,
            is_delivered=order_item_model.is_delivered,
            added_at=order_item_model.added_at
        )