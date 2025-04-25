from injector import inject
from ...core.domain.entities.order_entity import Order, OrderItem
from ...core.repositories.order_repository import OrderRepository
from ...core.repositories.table_repository import TableRepository
from ..dtos.order_dto import OrderDTO
from ...core.mappers.order_mappers import OrderMapper
from typing import List, Dict, Any

class AddOrderItemsUseCase:
    @inject
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def execute(self, order_id : int, items_validate_data : List[Dict[str, Any]]) -> None:
        pass

class RemoveOrderItemUseCase:
    @inject
    def __init__(self, order_repository: OrderRepository, table_repository : TableRepository):
        self.order_repository = order_repository
        self.table_repository = table_repository

    def execute(self, order_id : int, items_validate_data : List[int]) -> None:
        pass


class UpdateOrderItemUseCase:
    @inject
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def execute(self, item_id : int, order_item_data : dict):
        pass

