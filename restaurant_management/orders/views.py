from rest_framework.viewsets import ModelViewSet
from .models import Order
from core.response.django_response import DjangoResponseWrapper as ResponseWrapper
from .serializers import OrderSerializer
import logging
from .services.order_service import OrderService

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
    