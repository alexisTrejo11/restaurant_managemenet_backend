from datetime import datetime
from typing import List, Optional
from restaurant.utils.exceptions import DomainException
from restaurant.services.domain.menu_item import MenuItem
from restaurant.services.domain.menu_extra import MenuExtraDomain

class OrderStatus:
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'


class OrderItem:
    def __init__(self, 
                 menu_item: MenuItem, 
                 menu_extra: MenuExtraDomain = None, 
                 added_at: Optional[datetime] = None, 
                 notes: Optional[str] = None, 
                 quantity: int = 1, 
                 id: Optional[int] = None, 
                 is_delivered: bool = False):
        self.__id = id
        self.__menu_item = menu_item
        self.__quantity = quantity
        self.__notes = notes
        self.__menu_extra = menu_extra
        self.__is_delivered = is_delivered
        self.__added_at = added_at or datetime.now()

    def __str__(self):
        return f"{self.__menu_item.name}"

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value: Optional[int]):
        self.__id = value

    @property
    def menu_item(self):
        return self.__menu_item

    @menu_item.setter
    def menu_item(self, value: MenuItem):
        self.__menu_item = value

    @property
    def quantity(self):
        return self.__quantity

    @quantity.setter
    def quantity(self, value: int):
        self.__quantity = value

    @property
    def notes(self):
        return self.__notes

    @notes.setter
    def notes(self, value: Optional[str]):
        self.__notes = value

    @property
    def menu_extra(self):
        return self.__menu_extra

    @menu_extra.setter
    def menu_extra(self, value: Optional[MenuExtraDomain]):
        self.__menu_extra = value

    @property
    def is_delivered(self):
        return self.__is_delivered

    @is_delivered.setter
    def is_delivered(self, value: bool):
        self.__is_delivered = value

    @property
    def added_at(self):
        return self.__added_at

    @added_at.setter
    def added_at(self, value: Optional[datetime]):
        self.__added_at = value

    def mark_delivered(self):
        self.__is_delivered = True

    def format_notes(self, new_quantity: int, new_notes: Optional[str]):
        formatted_new_notes = f"{new_quantity}: {new_notes if new_notes else ''}"
        if not self.__notes:
            self.__notes = formatted_new_notes    
        else:
            self.__notes = f"{self.__notes} || {formatted_new_notes}"


class Order:
    def __init__(
        self, 
        table, 
        status: str, 
        created_at: Optional[datetime] = None, 
        end_at: Optional[datetime] = None, 
        id: Optional[int] = None, 
        items: List[OrderItem] = None
    ):
        self.__id = id
        self.__table = table 
        self.__status = status
        self.__created_at = created_at or datetime.now()
        self.__end_at = end_at
        self.__items = items or []

    def __str__(self):
        return f"Order {self.__id} - Table {self.__table.number}"

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value: Optional[int]):
        self.__id = value

    @property
    def table(self):
        return self.__table

    @table.setter
    def table(self, value):
        self.__table = value

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value: str):
        self.__status = value

    @property
    def created_at(self):
        return self.__created_at

    @created_at.setter
    def created_at(self, value: Optional[datetime]):
        self.__created_at = value

    @property
    def end_at(self):
        return self.__end_at

    @end_at.setter
    def end_at(self, value: Optional[datetime]):
        self.__end_at = value

    @property
    def items(self):
        return self.__items

    @items.setter
    def items(self, value: List[OrderItem]):
        self.__items = value

    def set_item_as_delivered(self, item_id: int):
        is_marked = False
        for item in self.__items:
            if item.id == item_id:
                item.mark_delivered()
                is_marked = True
        
        if not is_marked:
            raise DomainException('Item not found to be set as delivered')

    def set_as_cancel(self):
        if self.__status != OrderStatus.IN_PROGRESS:
            raise DomainException('Only in progress orders can be cancelled')
        self.__status = OrderStatus.CANCELLED
        self.__end_at = datetime.now()

    def set_as_complete(self):
        if self.__status != OrderStatus.IN_PROGRESS:
            raise DomainException('Only in progress orders can be ended')
        self.__status = OrderStatus.COMPLETED
        self.__end_at = datetime.now()

    def add_item(self, order_item: OrderItem) -> OrderItem:
        self.__items.append(order_item)
        return order_item

    def add_items(self, new_items: List[OrderItem]):
        self.__items.extend(new_items)

    def is_order_in_progress(self) -> bool:
        return self.__status == OrderStatus.IN_PROGRESS

    def remove_items(self, item_ids: List[int]):
        removed_items = []
        remaining_items = []

        for item in self.__items:
            if item.id in item_ids:
                removed_items.append(item)
            else:
                remaining_items.append(item)

        found_ids = {item.id for item in removed_items}
        missing_ids = set(item_ids) - found_ids
        if missing_ids:
            raise ValueError(f"Items with IDs {missing_ids} not found in order")

        self.__items = remaining_items
