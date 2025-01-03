from typing import List
from restaurant.repository.order_repository import OrderRepository
from restaurant.services.domain.order import Order, OrderStatus, OrderItem
from restaurant.services.domain.table import Table
from restaurant.repository.table_respository import TableRepository
from restaurant.repository.menu_item_repository import MenuItemRepository
from injector import inject

class OrderService:
    @inject
    def __init__(
        self, 
        order_repository : OrderRepository, 
        table_repository : TableRepository,
        menu_item_repository : MenuItemRepository,
        ):
        self.order_repository = order_repository
        self.table_repository = table_repository
        self.menu_item_repository = menu_item_repository
    

    def get_order_by_id(self, order_id):
        return self.order_repository.get_by_id(order_id)


    def get_orders_by_status(self, status) -> List[Order]:
        return self.order_repository.get_by_status(status)
    

    def init_order(self, table: Table) -> Order:
        new_order = Order(
            status=OrderStatus.IN_PROGRESS, 
            table=table
        )

        self.table_repository.set_as_unavailable(new_order.table.number)
        
        return self.order_repository.create(new_order)
    

    def proccess_items(self, items_data):
        created_items = []
        
        for item_data in items_data: 
            menu_item_id = item_data.get('menu_item_id')  
            quantity = item_data.get('quantity') 
            notes = item_data.get('notes') 

            menu_item = self.menu_item_repository.get_by_id(menu_item_id)
            if not menu_item:
                raise ValueError(f'Menu Item with [{menu_item_id}] not found')

            order_item = OrderItem(

                menu_item=menu_item,
                quantity=quantity,
                notes=notes
            )
            created_items.append(order_item)

        return created_items


    def add_items_to_order(self, order: Order, order_items: List[OrderItem]) -> Order:
        order.add_items(order_items)

        return self.order_repository.update_items(order)
    

    def delete_items_to_order(self, order: Order, item_ids: List[int]) -> Order:
        order.remove_items(item_ids)

        self.order_repository.update_items(order)

        return order


    def delete_order_by_id(self, order_id):
        return self.order_repository.delete(order_id)


    def cancel_order(self, order: Order):
        order.set_as_cancel()

        self.order_repository.update(order)
        self.table_repository.set_as_unavailable(order.table.number)


    def end_order(self, order: Order):
        order.set_as_complete()

        self.table_repository.set_as_unavailable(order.table.number)
        return self.order_repository.update(order)


    def set_item_as_delivered(self, order_id, item_id):
        order = self.order_repository.get_by_id(order_id)
        order.set_item_as_delivered(item_id)
        
        self.order_repository.update_items(order)


    def get_not_delivered_items(self):
        return self.order_repository.get_not_delivered_items()