from ..models import OrderItem, Order
from typing import List
from core.exceptions.custom_exceptions import BusinessRuleViolationException
class OrderItemService:
    MAX_ALLOWED_ITEMS_PER_REQUEST = 10
    
    def add_items(cls, order: Order, items_validated_data: List) -> Order:
        cls._validate_item_lenght_limit(items_validated_data)
        items = cls._generate_items(order, items_validated_data)

        OrderItem.objects.bulk_create(items)
        order.items = items

        return order
    

    def delete_items(cls, items: List[OrderItem]):
        for item in items:
            item.delete()

    def _generate_items(cls, order: Order, items_data: List[str, any]) ->  List[OrderItem]:
        items = []
        for item in items_data:
            OrderItem(
                order=order,
                menu_item=item.get('menu_item'),
                quantity=item.get('quantity'),
                notes=item.get('notes'),
                is_delivered=False
            )
            items.append(item)
        return items

    def _validate_item_lenght_limit(cls, items: List):
        if len(items) > cls.MAX_ALLOWED_ITEMS_PER_REQUEST:
            raise BusinessRuleViolationException("Can't Procces more than 10 dishes at the same time")


    