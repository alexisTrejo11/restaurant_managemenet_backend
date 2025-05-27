from shared.response.django_response import DjangoResponseWrapper as ResponseWrapper
from ..serializers import OrderItemSerializer
from ..services.order_service import OrderService
from ..services.order_item_service import OrderItemService
from rest_framework.decorators import api_view
import logging

logger = logging.getLogger(__name__)

# TODO: Add Permisions
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

@api_view(['POST'])
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
