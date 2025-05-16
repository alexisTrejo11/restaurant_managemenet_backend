from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime
from ...domain.entities.table_entity import Table

@dataclass
class OrderItem:
    """
    Domain entity representing an item within an order.
    """
    menu_item_id: int = None
    order_id: Optional[int] = None
    menu_extra_id: Optional[int] = None
    quantity: int = 1
    notes: Optional[str] = None
    is_delivered: bool = False
    added_at: Optional[datetime] = None

    def __str__(self):
        return f"MenuItem {self.menu_item_id} - Order {self.order_id if self.order_id else 'Unknown'}"


@dataclass
class Order:
    """
    Domain entity representing an order placed at a table.
    """
    id: Optional[int] = None
    table: 'Table' = None
    status: str = "IN_PROGRESS"
    created_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    order_items : List[OrderItem] = field(default_factory=list)

    def __str__(self):
        return f"Order {self.id} - Table {self.table.number}"

    @staticmethod
    def start(table : 'Table', items : List[OrderItem] = []):
        return Order(
            table=table,
            created_at= datetime.now(),
            order_items=items,
        )

    def update(self, updated_data : dict) -> None:
        pass

    def update_items(self, items : List[OrderItem]) -> None:
        pass

    def get_new_items(self, incoming_items : List[OrderItem]) -> List[OrderItem]:
        pass

    def add_items(self, incoming_items : dict) -> None :
        self.order_items.append(incoming_items)
