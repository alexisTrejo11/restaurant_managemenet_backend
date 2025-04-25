from injector import inject
from ...core.domain.entities.order_entity import Order, OrderItem
from ...core.repositories.order_repository import OrderRepository
from ...core.repositories.table_repository import TableRepository
from ..dtos.order_dto import OrderDTO
from ...core.mappers.order_mappers import OrderMapper
from typing import List

class StartOrderUseCase:
    """
    Use case for start a new order.
    """
    @inject
    def __init__(self, order_repository: OrderRepository, table_repository : TableRepository):
        self.order_repository = order_repository
        self.table_repository = table_repository

    def execute(self, table_number : int, items : List[OrderItem] = []) -> OrderDTO:
        table = self.table_repository.get_by_id(table_number, raise_exception=True)
        if not table.is_available:
            raise ValueError('Table is occupied')

        new_order = Order.start(table_number, items)
        self.order_repository.validate_not_conflict(new_order)
        
        order_created = self.order_repository.save(new_order)

        return OrderMapper.domain_to_dto(order_created)


class EndOrderUseCase:
    """
    Use case for start a new order.
    """
    @inject
    def __init__(self, order_repository: OrderRepository, table_repository : TableRepository):
        self.order_repository = order_repository
        self.table_repository = table_repository

    def execute(self, table_number : int, items : List[OrderItem] = []) -> OrderDTO:
        table = self.table_repository.get_by_id(table_number, raise_exception=True)
        if not table.is_available:
            raise ValueError('Table is occupied')

        new_order = Order.start(table_number, items)
        self.order_repository.validate_not_conflict(new_order)
        
        order_created = self.order_repository.save(new_order)

        return OrderMapper.domain_to_dto(order_created)


class CreateOrderUseCase:
    """
    Use case for creating a new order.
    """
    @inject
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def execute(self, order_validated_data: dict) -> OrderDTO:
        new_order = OrderMapper.dict_to_domain(order_validated_data)
        
        order_created = self.order_repository.save(new_order)
        
        return OrderMapper.domain_to_dto(order_created)    

class UpdateOrderUseCase:
    """
    Use case for updating an existing order.
    """
    @inject
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def execute(self, exisiting_order: Order, order_updated_data : dict) -> OrderDTO:
        exisiting_order.update(order_updated_data)

        order_updated = self.order_repository.save(exisiting_order)
        return OrderMapper.domain_to_dto(order_updated)


class DeleteOrderUseCase:
    """
    Use case for deleting an order.
    """
    @inject
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def execute(self, id: int) -> bool:
        """
        Delete an order from the repository.
        
        Args:
            id (int): The ID of the order to delete.
        
        Returns:
            None
        """
        order = self.order_repository.get_by_id(id, raise_exception=True)
        return self.order_repository.delete(order.id)