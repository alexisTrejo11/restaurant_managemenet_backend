from typing import List, Optional, Dict
from ...core.domain.entities.order_entity import Order, OrderItem
from ...core.repositories.order_repository import OrderRepository
from ..models.order_model import OrderModel
from ..models.order_item_model import OrderItemModel
from ...core.mappers.order_mappers import OrderMapper, OrderItemMapper
from shared.cache.django_cache_manager import CacheManager
from django.db.models import Q
from shared.exceptions.custom_exceptions import EntityNotFoundException


ORDER_CACHE_PREFIX = "ORDER_"
ORDER_ALL_CACHE_PREFIX = "ORDER_ALL"

class DjangoOrderRepository(OrderRepository):
    def __init__(self):
        self.cache_manager = CacheManager(ORDER_CACHE_PREFIX)
        super().__init__()

    def get_by_id(self, id: int, raise_exception=False) -> Optional[Order]:
        """
        Retrieve an order by its ID, checking the cache first.
        
        Args:
            id (int): The ID of the order to retrieve.
            raise_exception (bool): Whether to raise an exception if the order is not found.
        
        Returns:
            Optional[Order]: The retrieved order, or None if not found and raise_exception is False.
        """
        order_cache = self._get_by_id_cache(id)
        if order_cache:
            return order_cache

        return self._get_by_id_db(id, raise_exception)

    def get_all(self) -> List[Order]:
        """
        Retrieve all orders, checking the cache first.
        
        Returns:
            List[Order]: A list of all orders.
        """
        orders_cache = self._get_query_set_from_cache()
        if orders_cache:
            return orders_cache

        orders = OrderModel.objects.all().order_by('id')
        orders_list = [OrderMapper.to_domain(model) for model in orders]

        # Cache the result
        self.cache_manager.set(ORDER_ALL_CACHE_PREFIX, orders_list)

        return orders_list
    
    def search(self, filters: Dict[str, any]) -> List[Order]:
        """
        Perform a dynamic filtering and search operation on orders.
        
        Args:
            filters (Dict[str, any]): A dictionary of filters where keys are field names 
                                      and values are the corresponding filter values.
                                      Supports nested fields (e.g., 'table__number').

        Returns:
            List[Order]: A list of filtered Order domain entities.
        """
        query = Q()

        # Dynamically build the query based on the provided filters
        for key, value in filters.items():
            if value is not None:
                query &= Q(**{key: value})

        order_models = OrderModel.objects(query).order_by('-created_at')

        return [OrderMapper.to_domain(model) for model in order_models]

    def create(self, order: Order) -> Order:
        """
        Create a new order and save it to the database and cache.
        
        Args:
            order (Order): The order entity to create.
        
        Returns:
            Order: The created order.
        """
        order_model = OrderMapper.to_model(order)
        order_model.save()

        created_order = OrderMapper.to_domain(order_model)

        cache_key = self.cache_manager.get_cache_key(created_order.id)
        self.cache_manager.set(cache_key, created_order)
        self._refresh_query_set_cache()

        return created_order

    def update(self, order: Order) -> Order:
        """
        Update an existing order in the database and cache.
        
        Args:
            order (Order): The order entity to update.
        
        Returns:
            Order: The updated order.
        """
        order_model = OrderModel.objects.filter(id=order.id).first()
        if not order_model:
            raise ValueError(f"Order with id {order.id} not found")

        updated_model = OrderMapper.to_model(order)
        for field, value in updated_model.__dict__.items():
            if field != 'id' and not field.startswith('_'):
                setattr(order_model, field, value)

        order_model.save()

        updated_order = OrderMapper.to_domain(order_model)

        cache_key = self.cache_manager.get_cache_key(updated_order.id)
        self.cache_manager.set(cache_key, updated_order)
        self._refresh_query_set_cache()

        return updated_order

    def delete(self, id: int) -> bool:
        """
        Delete an order from the database and cache.
        
        Args:
            id (int): The ID of the order to delete.
        
        Returns:
            bool: True if the order was deleted, False otherwise.
        """
        deleted, _ = OrderModel.objects.filter(id=id).delete()

        cache_key = self.cache_manager.get_cache_key(id)
        self.cache_manager.delete(cache_key)
        self._refresh_query_set_cache()

        return deleted > 0

    def get_by_status(self, status: str) -> List[Order]:
        """
        Retrieve all orders with a specific status.
        
        Args:
            status (str): The status to filter orders by.
        
        Returns:
            List[Order]: A list of orders matching the status.
        """
        models = OrderModel.objects.filter(status=status)
        return [OrderMapper.to_domain(model) for model in models]

    def get_not_delivered_items(self) -> List[OrderItem]:
        """
        Retrieve all order items that have not been delivered.
        
        Returns:
            List[OrderItem]: A list of undelivered order items.
        """
        model_items = OrderItemModel.objects.filter(is_delivered=False)
        return [OrderItemMapper.to_domain(model_item) for model_item in model_items]


    def _get_by_id_cache(self, id: int) -> Optional[Order]:
        """
        Retrieve an order by its ID from the cache.
        
        Args:
            id (int): The ID of the order to retrieve.
        
        Returns:
            Optional[Order]: The cached order, or None if not found.
        """
        cache_key = self.cache_manager.get_cache_key(id)
        return self.cache_manager.get(cache_key)

    def _get_by_id_db(self, id: int, raise_exception=False) -> Optional[Order]:
        """
        Retrieve an order by its ID from the database.
        
        Args:
            id (int): The ID of the order to retrieve.
            raise_exception (bool): Whether to raise an exception if the order is not found.
        
        Returns:
            Optional[Order]: The retrieved order, or None if not found and raise_exception is False.
        """
        try:
            model = OrderModel.objects.get(id=id)
            return OrderMapper.to_domain(model)
        except OrderModel.DoesNotExist:
            if raise_exception:
                raise EntityNotFoundException("Order", id)
            else:
                return None

    def _get_query_set_from_cache(self) -> List[Order]:
        """
        Retrieve all orders from the cache.
        
        Returns:
            List[Order]: A list of cached orders, or None if not found.
        """
        orders_cache = self.cache_manager.get(ORDER_ALL_CACHE_PREFIX)
        if orders_cache:
            return [OrderMapper.to_domain(model) for model in orders_cache]
        return None

    def _refresh_query_set_cache(self):
        """
        Refresh the cache for all orders.
        """
        orders = OrderModel.objects.all().order_by('id')
        orders_list = [OrderMapper.to_domain(model) for model in orders]
        self.cache_manager.set(ORDER_ALL_CACHE_PREFIX, orders_list)
