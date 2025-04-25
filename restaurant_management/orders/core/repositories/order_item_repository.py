from core.repository.common_repository import CommonRepository
from abc import ABC, abstractmethod
from typing import Optional
from ...core.domain.entities.order_entity import Order, OrderItem

class OrderItemRepository:
    @abstractmethod
    def update_order_items(self, order: Order) -> None:
        pass
    
    @abstractmethod
    def get_by_id(self, item_id: int, raise_expcetion=False) -> Optional[OrderItem]:
        pass

    @abstractmethod
    def save(self, order_item: OrderItem) -> OrderItem:
        pass
     