from ..models import Order
from shared.exceptions.custom_exceptions import BusinessRuleViolationException, EntityNotFoundException
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

class OrderService:
    @classmethod
    def get_order(cls, order_id: int) -> Order:
        try:
            order = Order.objects.get(id=order_id)
            return order
        except Order.DoesNotExist:
            logger.error(f"Order with ID {order_id} does not exist.")
            raise EntityNotFoundException(f"Order", order_id)
    
    @classmethod
    def start_order(cls, validated_data: dict) -> Order:
        """
        Creates a new order instance after performing all necessary validations.
        """
        table = validated_data.get('table')
        if not table.is_available:
            raise BusinessRuleViolationException("Table is not available for new orders.")

        status = validated_data.get('status')
        if status != 'IN_PROGRESS':
            raise BusinessRuleViolationException("Order status must be 'IN_PROGRESS' when starting a new order.")
        
        try:
            with transaction.atomic():
                order = Order.objects.create(**validated_data)
                cls._take_table(order)
                return order
        except Exception as e:
            logger.error(f"Error creating order with data {validated_data}: {e}", exc_info=True)
            raise

    @classmethod
    def update_order(cls, order: Order, new_status=None, new_table=None) -> Order:
        """
        Updates an existing order instance after performing all necessary validations.
        """
        try:
            with transaction.atomic():
                order.save()
                return order
        except Exception as e:
            logger.error(f"Error updating order ID {order.id} {e}", exc_info=True)
            raise

    @classmethod
    def delete_order(cls, order: Order):
        """
        Deletes an order instance after performing all necessary validations.
        """
        cls._validate_order_in_progress(order)

        try:
            with transaction.atomic():
                cls._clear_table(order)
                order.delete()
        except Exception as e:
            logger.error(f"Error deleting order ID {order.id}: {e}", exc_info=True)
            raise
    
    @classmethod
    def update_order_status(cls, order: Order, new_status: str):
        cls._validate_order_in_progress(order)
        
        if new_status:
            if new_status == 'COMPLETED':
                cls.complete_order()
            elif new_status == 'CANCELLED':
                cls.cancel_order()


    @classmethod
    def complete_order(cls, order: Order):
        cls._validate_order_in_progress(order)
        order.complete()
        order.save()
        cls._clear_table(order)
        return order

    @classmethod
    def cancel_order(cls, order: Order):
        cls._validate_order_in_progress(order)
        order.cancel()
        order.save()
        cls._clear_table(order)    

    @classmethod
    def _update_order_table(cls, order: Order, new_table):
        if new_table != order.table:            
            if not new_table.is_available:
                raise BusinessRuleViolationException("Table is not available for new orders.")
            order.table = new_table
            cls._take_table(order)
    
    @classmethod
    def _validate_order_in_progress(cls, order: Order):    
        if order.status != 'IN_PROGRESS':
            raise BusinessRuleViolationException("Compelted or Cancelled Order can change their status")
    
    @classmethod
    def _clear_table(cls, order: Order):
        table = order.table
        table.is_available = True
        table.save()

    @classmethod
    def _take_table(cls, order: Order):
        table = order.table
        table.is_available = False
        table.save()