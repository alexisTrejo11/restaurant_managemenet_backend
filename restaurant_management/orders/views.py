from rest_framework.viewsets import ModelViewSet
from .models import Order
from core.response.django_response import DjangoResponseWrapper as ResponseWrapper
from .serializers import OrderSerializer, OrderItemSerializer
import logging
from .services.order_service import OrderService
from .services.order_item_service import OrderItemService
from rest_framework.decorators import api_view, permission_classes 

# TODO: Add Permisions

logger = logging.getLogger(__name__)

class OrderViewsSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = []

    def list(self, request, *args, **kwargs):
        user_id = getattr(request.user, 'id', 'Anonymous') 
        logger.info(f"User {user_id} is requesting order list.")
        
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        logger.info(f"Returning {len(queryset)} tables.")
        return ResponseWrapper.found(
            data=serializer.data,
            entity="Order List",
        )

    def retrieve(self, request, *args, **kwargs):
        order = self.get_object()
        user_id = getattr(request.user, 'id', 'Anonymous') 
        logger.info(f"User {user_id} is requesting retriving order {order.id}.")
        
        serializer = self.get_serializer(order)
        
        logger.info(f"Returning details for order ID: {order.id}.")
        return ResponseWrapper.found(
            data=serializer.data,
            entity=f"Order {order.id}",
        )

    def create(self, request, *args, **kwargs):
        user_id = getattr(request.user, 'id', 'Anonymous') 
        logger.info(f"User {user_id} is requesting creating order.")
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = OrderService.start_order(serializer.validated_data)
        
        logger.info(f"Order ID: {order.id} created successfully.")
        serializer = self.get_serializer(order)
        return ResponseWrapper.created(
            data=serializer.data,
            entity=f"Order {order.id}",
        )
    
    def update(self, request, *args, **kwargs):
        order = self.get_object()
        user_id = getattr(request.user, 'id', 'Anonymous')
        logger.info(f"User {user_id} is requesting updating order {order.id}.")

        new_status = request.query_params.get('status')
        new_table = request.query_params.get('table_id')
        
        order_updated = OrderService.update_order(order, new_status, new_table)
        logger.info(f"Order ID: {order.id} updated successfully.")
        
        serializer = self.get_serializer(order_updated)
        return ResponseWrapper.updated(
            data=serializer.data,
            entity=f"Order {order.id}",
        )

    def destroy(self, request, *args, **kwargs):
        order = self.get_object()
        order_id = order.id
        user_id = getattr(request.user, 'id', 'Anonymous') 
        logger.info(f"User {user_id} is requesting deleting order {order_id}.")
        
        OrderService.delete_order(order)
        
        logger.info(f"Order ID: {order_id} deleted successfully.")
        return ResponseWrapper.deleted(
            entity=f"Order {order_id}",
        )
    

@api_view(['POST'])
def add_order_item(request, order_id):
    """
    API endpoint to add items to an order
    """
    if not order_id:
        return ResponseWrapper.bad_request(message="Order ID is required")

    user_id = request.user.id if request.user.is_authenticated else 'Anonymous'
    logger.info(
        f"User {user_id} adding items to order {order_id}",
        extra={'data': request.data}
    )

    order = OrderService.get_order(order_id)
    serializer = OrderItemSerializer(data=request.data, many=True)
    serializer.is_valid(raise_exception=True)
    
    updated_order = OrderItemService.add_items(order, serializer.validated_data)
    
    logger.info(
        f"Items added to order {order_id} by user {user_id}",
        extra={'item_count': len(serializer.validated_data)}
    )
    
    return ResponseWrapper.created(
        data=OrderItemSerializer(updated_order.order_items.all(), many=True).data,
        entity=f"Order {order_id} Items"
    )

@api_view(['DELETE'])
def delete_order_item(request, order_id): 
    """
    API endpoint to delete items from an order
    """
    order_items_ids = request.data.get('order_item_ids', [])
    
    if not order_id or not order_items_ids:
        return ResponseWrapper.bad_request(
            message="Both Order ID and Order Item IDs are required"
        )

    user_id = request.user.id if request.user.is_authenticated else 'Anonymous'
    logger.info(
        f"User {user_id} removing items from order {order_id}",
        extra={'item_ids': order_items_ids}
    )

    order = OrderService.get_order(order_id)
    OrderItemService.delete_items(order, order_items_ids)
    
    logger.info(
        f"Items removed from order {order_id} by user {user_id}",
        extra={'item_ids': order_items_ids}
        )
    
    return ResponseWrapper.deleted(
        entity=f"Order Items {order_items_ids}"
        )
