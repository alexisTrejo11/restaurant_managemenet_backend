from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from ...domain.entities.table_entitiy import Table

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

    def __str__(self):
        return f"Order {self.id} - Table {self.table.number}"


@dataclass
class OrderItem:
    """
    Domain entity representing an item within an order.
    """
    menu_item_id: int
    order_id: Optional[int] = None
    menu_extra_id: Optional[int] = None
    quantity: int = 1
    notes: Optional[str] = None
    is_delivered: bool = False
    added_at: Optional[datetime] = None

    def __str__(self):
        return f"MenuItem {self.menu_item_id} - Order {self.order_id if self.order_id else 'Unknown'}"