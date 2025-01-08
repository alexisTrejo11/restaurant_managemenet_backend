from datetime import datetime
from pickle import TRUE
from typing import List, Optional
from restaurant.utils.exceptions import DomainException

class OrderStatus:
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'


class OrderItem:
    def __init__(self, 
                menu_item, 
                added_at = datetime.now(), 
                notes=None, quantity=1, 
                id=None, 
                menu_extra=None, 
                is_delivered=False):
        self.id = id
        self.menu_item = menu_item
        self.quantity = quantity
        self.notes = notes
        self.menu_extra = menu_extra
        self.is_delivered = is_delivered
        self.added_at = added_at

    def __str__(self):
        return f"{self.menu_item.name}"

    def mark_delivered(self):
        self.is_delivered = True


    def format_notes(self, new_quantity: int, new_notes: Optional[str]):
        formatted_new_notes = f"{new_quantity}: {new_notes if new_notes else ''}"
        if not self.notes:
            self.notes = formatted_new_notes    
        else:
            self.notes = f"{self.notes} || {formatted_new_notes}"


class Order:
    def __init__(
        self, 
        table, 
        status: str, 
        created_at: Optional[datetime] = None, 
        end_at: Optional[datetime] = None, 
        id=None, 
        items: List[OrderItem] = []
    ):
        self.id = id
        self.table = table 
        self.status = status
        self.created_at = created_at or datetime.now()
        self.end_at = end_at
        self.items = items

    def __str__(self):
        return f"Order {self.id} - Table {self.table.number}"

    def set_item_as_delivered(self, item_id):
        is_marked = False
        for item in self.items:
            if item.id == item_id:
                item.mark_delivered()
                is_marked = True
        
        if not is_marked:
            raise DomainException('Item not found to be set as delivered')


    def set_as_cancel(self):
        if self.status != OrderStatus.IN_PROGRESS:
            raise DomainException('Only in progress orders can be cancelled')
        self.status = OrderStatus.CANCELLED
        self.end_at = datetime.now()


    def set_as_complete(self):
        if self.status != OrderStatus.IN_PROGRESS:
            raise DomainException('Only in progress orders can be ended')
        self.status = OrderStatus.COMPLETED
        self.end_at = datetime.now()


    def add_item(self, order_item: OrderItem) -> OrderItem:
        self.items.append(order_item)
        return order_item


    def add_items(self, new_items: List[OrderItem]):
        self.items.extend(new_items)


    def remove_items(self, item_ids: List[int]):
        removed_items = []
        remaining_items = []

        for item in self.items:
            if item.id in item_ids:
                removed_items.append(item)
            else:
                remaining_items.append(item)

        found_ids = {item.id for item in removed_items}
        missing_ids = set(item_ids) - found_ids
        if missing_ids:
            raise ValueError(f"Items with IDs {missing_ids} not found in order")

        self.items = remaining_items
