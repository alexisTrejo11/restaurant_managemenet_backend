from ..domain.entities.table_entity import Table
from ..domain.entities.order_entity import Order
from ...application.dtos.order_dto import OrderDTO
from ...models import OrderModel
from ..domain.entities.order_entity import OrderItem
from ...application.dtos.order_dto import OrderItemDTO
from ...models import OrderItemModel

class OrderMapper:
    """
    Mapper class for converting between Order domain entities, DTOs, and Django models.
    """

    @staticmethod
    def domain_to_dto(order: Order) -> OrderDTO:
        """
        Maps an Order domain entity to an OrderDTO.
        
        Args:
            order (Order): The Order domain entity to map.
        
        Returns:
            OrderDTO: The corresponding OrderDTO.
        """
        return OrderDTO(
            id=order.id,
            table_number=order.table.number,
            status=order.status,
            created_at=order.created_at,
            end_at=order.end_at,
        )

    @staticmethod
    def dict_to_domain(data: dict, table: Table) -> Order:
        """
        Maps a dictionary representation to an Order domain entity.
        
        Args:
            data (dict): A dictionary containing the serialized data for the Order.
            table (Table): The associated Table domain entity.
        
        Returns:
            Order: The corresponding Order domain entity.
        """
        return Order(
            id=data.get('id'),
            table=table,
            status=data.get('status'),
            created_at=data.get('created_at'),
            end_at=data.get('end_at'),
        )

    @staticmethod
    def domain_to_model(order: Order) -> OrderModel:
        """
        Maps an Order domain entity to an OrderModel (Django model).
        
        Args:
            order (Order): The Order domain entity to map.
        
        Returns:
            OrderModel: The corresponding Django model instance.
        """
        return OrderModel(
            id=order.id,
            table_id=order.table.number,  # Assuming `table` has a `number` field as the primary key in the database
            status=order.status,
            created_at=order.created_at,
            end_at=order.end_at,
        )

class OrderItemMapper:
    """
    Mapper class for converting between OrderItem domain entities, DTOs, and Django models.
    """

    @staticmethod
    def domain_to_dto(order_item: OrderItem) -> OrderItemDTO:
        """
        Maps an OrderItem domain entity to an OrderItemDTO.
        
        Args:
            order_item (OrderItem): The OrderItem domain entity to map.
        
        Returns:
            OrderItemDTO: The corresponding OrderItemDTO.
        """
        return OrderItemDTO(
            menu_item_id=order_item.menu_item_id,
            order_id=order_item.order_id,
            menu_extra_id=order_item.menu_extra_id,
            quantity=order_item.quantity,
            notes=order_item.notes,
            is_delivered=order_item.is_delivered,
            added_at=order_item.added_at,
        )

    @staticmethod
    def dict_to_domain(data: dict) -> OrderItem:
        """
        Maps a dictionary representation to an OrderItem domain entity.
        
        Args:
            data (dict): A dictionary containing the serialized data for the OrderItem.
        
        Returns:
            OrderItem: The corresponding OrderItem domain entity.
        """
        return OrderItem(
            menu_item_id=data.get('menu_item_id'),
            order_id=data.get('order_id'),
            menu_extra_id=data.get('menu_extra_id'),
            quantity=data.get('quantity', 1),  # Default quantity is 1 if not provided
            notes=data.get('notes'),
            is_delivered=data.get('is_delivered', False),  # Default is False if not provided
            added_at=data.get('added_at'),
        )

    @staticmethod
    def domain_to_model(order_item: OrderItem) -> OrderItemModel:
        """
        Maps an OrderItem domain entity to an OrderItemModel (Django model).
        
        Args:
            order_item (OrderItem): The OrderItem domain entity to map.
        
        Returns:
            OrderItemModel: The corresponding Django model instance.
        """
        return OrderItemModel(
            menu_item_id=order_item.menu_item_id,
            order_id=order_item.order_id,
            menu_extra_id=order_item.menu_extra_id,
            quantity=order_item.quantity,
            notes=order_item.notes,
            is_delivered=order_item.is_delivered,
            added_at=order_item.added_at,
        )