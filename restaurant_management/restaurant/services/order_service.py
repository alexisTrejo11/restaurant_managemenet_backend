from typing import List
from restaurant.repository.order_repository import OrderRepository
from restaurant.repository.menu_item_repository import MenuItemRepository
from restaurant.repository.menu_extra_repository import MenuExtraRepository
from restaurant.services.domain.order import Order, OrderStatus, OrderItem
from restaurant.services.domain.table import Table
from restaurant.repository.table_respository import TableRepository
from injector import inject
import logging

logger = logging.getLogger(__name__)

class OrderService:
    @inject
    def __init__(
        self, 
        order_repository : OrderRepository, 
        table_repository : TableRepository,
        menu_item_repository : MenuItemRepository,
        menu_extra_repository : MenuExtraRepository
        ):
        self.order_repository = order_repository
        self.table_repository = table_repository
        self.menu_extra_repository = menu_extra_repository
        self.menu_item_repository = menu_item_repository
    

    def get_order_by_id(self, order_id):
        return self.order_repository.get_by_id(order_id)


    def get_orders_by_status(self, status) -> List[Order]:
        return self.order_repository.get_by_status(status)
    
    
    def get_not_delivered_items(self):
        return self.order_repository.get_not_delivered_items()


    def init_order(self, table: Table) -> Order:
        new_order = Order(
            status=OrderStatus.IN_PROGRESS, 
            table=table
        )

        self.table_repository.set_as_unavailable(new_order.table.number)
        
        created_order = self.order_repository.create(new_order)
        logger.info(f"Order with ID {created_order.id} initiated successfully for table {table.number}.")
        
        return created_order


    def proccess_items(self, items_data):
        created_items = []
        
        for item_data in items_data: 
            menu_item_id = item_data.get('menu_item_id')  
            quantity = item_data.get('quantity') 
            notes = item_data.get('notes') 
            menu_extra_id =  item_data.get('menu_extra_id') 

            menu_item = self.menu_item_repository.get_by_id(menu_item_id)
            if not menu_item:
                raise ValueError(f'Menu Item with [{menu_item_id}] not found')

            order_item = OrderItem(
                menu_item=menu_item,
                quantity=quantity,
                notes=notes
            )

            # Add Extra if provided
            if menu_extra_id:
                menu_extra = self.menu_extra_repository.get_by_id(menu_extra_id)
                if not menu_item:
                   raise ValueError(f'Menu Extra with [{menu_extra_id}] not found')

                order_item.menu_extra = menu_extra

            created_items.append(order_item)

        logger.info(f"Processed {len(created_items)} items.")
        return created_items


    def add_items_to_order(self, order: Order, order_items: List[OrderItem]) -> Order:
        order.add_items(order_items)

        updated_order = self.order_repository.update_items(order)
        logger.info(f"Added {len(order_items)} items to order with ID {order.id}.")
        
        return updated_order


    def delete_items_to_order(self, order: Order, item_ids: List[int]) -> Order:
        order.remove_items(item_ids)

        self.order_repository.update_items(order)
        logger.info(f"Removed items with IDs {item_ids} from order with ID {order.id}.")
        
        return order


    def delete_order_by_id(self, order_id):
        is_deleted = self.order_repository.delete(order_id)

        if is_deleted:
            logger.info(f"Order with ID {order_id} deleted successfully.")
        
        return is_deleted


    def cancel_order(self, order: Order):
        order.set_as_cancel()

        self.order_repository.update(order)
        self.table_repository.set_as_unavailable(order.table.number)
        logger.info(f"Order with ID {order.id} canceled.")


    def end_order(self, order: Order):
        order.set_as_complete()

        self.table_repository.set_as_unavailable(order.table.number)
        updated_order = self.order_repository.update(order)
        logger.info(f"Order with ID {order.id} completed.")
        
        return updated_order


    def set_item_as_delivered(self, order_id, item_id):
        order = self.order_repository.get_by_id(order_id)
        order.set_item_as_delivered(item_id)
        
        self.order_repository.update_items(order)
        logger.info(f"Item with ID {item_id} set as delivered in order with ID {order.id}.")
