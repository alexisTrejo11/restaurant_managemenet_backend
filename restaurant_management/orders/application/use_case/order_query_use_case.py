from injector import inject
from typing import Optional, List
from ...core.domain.entities.order_entity import Order
from ...core.repositories.order_repository import OrderRepository
from ..dtos.order_dto import OrderDTO
from ...core.mappers.order_mappers import OrderMapper

class GetAllOrdersUseCase:
    """
    Use case for retrieving all orders.
    """
    @inject
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def execute(self) -> List[OrderDTO]:
        """
        Retrieve all orders from the repository.
        
        Returns:
            List[Order]: A list of all orders.
        """
        order_entity_list = self.order_repository.get_all()

        return [OrderMapper.domain_to_dto(order) for order in order_entity_list]


class GetOrderByIdUseCase:
    """
    Use case for retrieving an order by its ID.
    """
    @inject
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def execute(self, id: int, raise_exception=False) -> Optional[OrderDTO]:
        """
        Retrieve an order by its ID.
        
        Args:
            id (int): The ID of the order to retrieve.
            raise_exception (bool): Whether to raise an exception if the order is not found.
        
        Returns:
            Optional[Order]: The retrieved order, or None if not found and raise_exception is False.
        """
        order_entity = self.order_repository.get_by_id(id, raise_exception)
        if not order_entity:
            return None
        
        return OrderMapper.domain_to_dto(order_entity)


class SearchOrdersUseCase:
    @inject
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def execute(self, search_filters: dict = None) -> List[OrderDTO]:
        """
        Retrieve orders from the repository based on dynamic filters.
        
        Args:
            search_filters (dict): A dictionary of filter parameters to apply.
        
        Returns:
            List[OrderDTO]: A list of filtered OrderDTOs.
        """
        filters = self._validate_filter_params(search_filters)

        order_entity_list = self.order_repository.search(filters)

        return [OrderMapper.domain_to_dto(order) for order in order_entity_list]

    def _validate_filter_params(self, search_filters: dict) -> dict:
        """
        Validate and sanitize the filter parameters.
        
        Args:
            search_filters (dict): A dictionary of filter parameters provided by the user.
        
        Returns:
            dict: A sanitized dictionary of valid filter parameters.
        """
        allowed_fields = {
            'status',  # Status of the order (e.g., IN_PROGRESS, COMPLETED)
            'table__number',  # Table number associated with the order
            'created_at__gte',  # Orders created after a specific date
            'created_at__lte',  # Orders created before a specific date
            'end_at__isnull',  # Orders with or without an end date
        }

        valid_filters = {}

        if not search_filters:
            return valid_filters

        for key, value in search_filters.items():
            if key in allowed_fields and value is not None:
                valid_filters[key] = value

        return valid_filters
        