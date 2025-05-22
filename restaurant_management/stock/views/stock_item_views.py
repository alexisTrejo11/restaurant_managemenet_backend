from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.response.django_response import DjangoResponseWrapper as ResponseWrapper
from ..models import StockItem
import logging
from ..services.stock_item_service import StockItemService
from ..serializers import StockItemSerializer

logger = logging.getLogger(__name__)

class StockItemViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing stock item instances.
    """
    permission_classes = [IsAuthenticated]
    response_wrapper = ResponseWrapper
    serializer_class = StockItemSerializer
    queryset = StockItem.objects.all()

    def get_queryset(self):
        return super().get_queryset()

    def list(self, request, *args, **kwargs):
        user_id = getattr(request.user, 'id', 'Anonymous') 
        logger.info(f"User {user_id} is requesting stock item list.")

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        logger.info(f"Returning {len(queryset)} items.")
        return ResponseWrapper.found(
            data=serializer.data,
            entity="Stock List",
        )

        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user_id = getattr(request.user, 'id', 'Anonymous')
        logger.info(f"User {user_id} is requesting details for stock item ID: {instance.id}.")
        
        serializer = self.get_serializer(instance)

        logger.info(f"Returning details for stock item ID: {instance.id}.")
        return ResponseWrapper.found(
            data=serializer.data,
            entity=f"Stock Item {instance.id}",
        )
    
    def create(self, request, *args, **kwargs):
        user_id = getattr(request.user, 'id', 'Anonymous')
        logger.info(f"User {user_id} is attempting to create a new stock item with data: {request.data}.")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        created_stock_item = StockItemService.create_stock_item(serializer.validated_data)

        logger.info(f"Stock Item ID: {created_stock_item.id} created successfully by user {user_id}.")
        return ResponseWrapper.created(
            data=self.get_serializer(created_stock_item).data,
            entity=f"Stock Item {created_stock_item.id}",
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        user_id = getattr(request.user, 'id', 'Anonymous')
        logger.info(f"User {user_id} is attempting to update stock_item ID: {instance.id} with data: {request.data}.")

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        updated_stock_item = StockItemService.update_stock_item(instance, serializer.validated_data)

        logger.info(f"Stock Item ID: {updated_stock_item.id} updated successfully by user {user_id}.")
        return ResponseWrapper.updated(
            data=self.get_serializer(updated_stock_item).data,
            entity=f"Stock Item {updated_stock_item.id}",
        )    

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user_id = getattr(request.user, 'id', 'Anonymous')
        logger.info(f"User {user_id} is attempting to delete stock_item ID: {instance.id}.")

        stock_item_id = instance.id 
        StockItemService.delete_stock_item(instance)

        logger.info(f"Stock Item ID: {stock_item_id} deleted successfully by user {user_id}.")
        return ResponseWrapper.deleted(
            entity=f"Stock Item {stock_item_id}",
        )
