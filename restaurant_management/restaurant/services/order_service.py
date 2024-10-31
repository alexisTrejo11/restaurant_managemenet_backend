from restaurant.utils.result import Result
from restaurant.dtos.order_item_dtos import OrderItemInsertDTO
from restaurant.models import Order, OrderItem, Table
from django.db import transaction
from restaurant.models import Menu
from typing import List

class OrderService:
     @staticmethod
     def get_order_by_id(order_id):
          try:
               order = Order.objects.get(pk=order_id)
               return Result.success(order)
          except Order.DoesNotExist:
               return Result.error(f'order with ID {order_id} not found')


     @staticmethod
     def get_orders_by_status(order_status):
          if not Order.validate_status(order_status):
               return Result.error('Invalid order status')
          
          orders = Order.objects.filter(status=order_status).prefetch_related('items')
          return Result.success(orders)


     @staticmethod
     def delete_order_by_id(order_id):
          try:
               order = Order.objects.get(pk=order_id)
               order.delete()
               return Result.success(None)
          except Order.DoesNotExist:
               return Result.error(f'order with ID {order_id} not found')   


     @staticmethod
     def init_order(table: Table, order_items_dtos: list[OrderItemInsertDTO]):
          with transaction.atomic():
               OrderService.set_table_as_unavailable()

               order = Order(table=table, status='in_progress')
               order.save()
               
               order_items = OrderService._create_order_items(order, order_items_dtos)
               OrderService._save_order_items(order, order_items)
               return order
     
     
     @staticmethod
     def add_items_to_order(order: Order, order_items_dtos: List[OrderItemInsertDTO]):
        existing_items = OrderService.get_order_items(order)
        # Create dict using ids as key and items as values
        existing_items_dict = {item.menu_item.id: item for item in existing_items}
        
        items_to_add = []
        
        for dto in order_items_dtos:
            if dto.menu_id in existing_items_dict:
                # if items exists increase quantity
                existing_item = existing_items_dict[dto.menu_id]
                existing_item.quantity += dto.quantity
                items_to_add.append(existing_item) 
            else:
                # If not create new item
                menu_item = Menu.objects.get(pk=dto.menu_id)  # Cant produce exceptions
                new_item = OrderItem(order=order, menu_item=menu_item, quantity=dto.quantity)
                items_to_add.append(new_item)  
        
        # Save new and exisitng items
        if items_to_add:
            OrderItem.objects.bulk_create([item for item in items_to_add if isinstance(item, OrderItem) and item.pk is None])
            OrderItem.objects.bulk_update([item for item in items_to_add if isinstance(item, OrderItem) and item.pk is not None], ['quantity'])

        order.refresh_from_db() 
        return order


     @staticmethod
     def update_order_status(order: Order, order_status: str):       
          if not order.validate_status(order_status): 
               return   
          order.status = order_status
          order.save()
     

     @staticmethod
     def verify_order_cancel(order: Order):       
          if order.status is 'cancelled':
               return Result.error('Order already cancelled')
          elif order.status is 'pending_payment' or 'in_progress':
               return Result.error('Invalid order. Cannot be cancelled')
          else:
               return Result.success(None)


     @staticmethod
     def _create_order_items(order: Order, order_items_dtos: list[OrderItemInsertDTO]):
          order_items = []  
          for item_dto in order_items_dtos:
               menu_item = Menu.objects.get(pk=item_dto.menu_id)
               order_item = OrderItem(
                    order=order,
                    menu_item=menu_item,
                    quantity=item_dto.quantity
               )
               order_items.append(order_item)
          return order_items

     @staticmethod
     def _save_order_items(order: Order, order_items: list[OrderItem]):
          OrderItem.objects.bulk_create(order_items) 
          order.refresh_from_db()


     @staticmethod
     def get_order_items(order):
        return OrderItem.objects.filter(order=order)

     
     @staticmethod
     def set_table_as_unavailable(table: Table):
          table.set_as_unavailable()
          table.save()
     
     @staticmethod
     def set_table_as_available(table: Table):
          table.set_as_available()
          table.save()