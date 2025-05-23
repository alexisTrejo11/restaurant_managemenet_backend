from rest_framework.viewsets import ViewSet
from rest_framework.exceptions import NotFound
from core.response.django_response import DjangoResponseWrapper as ResponseWrapper
from rest_framework.permissions import IsAuthenticated
import logging
from ..models import Stock
from ..serializers import StockSerializer
from ..services.stock_service import StockService

logger = logging.getLogger(__name__)

class StockViews(ViewSet):
    queryset = Stock.objects.all()
    permission_classes = []
    serializer_class = StockSerializer

    def get_serializer_class(self):
        return StockSerializer
    
    def get_serializer(self, *args, **kwargs):
        """Send Request to serializer context"""
        serializer_class = self.get_serializer_class()
        kwargs['context'] = {'request': self.request}
        return serializer_class(*args, **kwargs)

    def list(self, request):
        queryset = self.queryset
        serializer = self.get_serializer(queryset, many=True)
        
        logger.info(f"Listed {len(queryset)} stock items")
        
        return ResponseWrapper.success(
            data=serializer.data,
            metadata={
                'total_items': queryset.count(),
                'note': 'Add ?include_transactions=true to include transactions'
            }
        )

    def retrieve(self, request, pk=None):
        stock = self.get_stock_or_404(pk)
        serializer = self.get_serializer(stock)
        
        logger.info(f"Retrieved stock {stock.id} with transactions={request.query_params.get('include_transactions')}")
        
        return ResponseWrapper.found(
            data=serializer.data,
            entity=f"Stock {stock.id} Details"
        )
    
    def create(self, request):
        serializer = self.get_serializer()
        serializer.is_valid(raise_exception=True)

        stock_created = StockService.create_stock(serializer.validated_data)

        stock_serialized = self.get_serializer(stock_created)
        return ResponseWrapper.created(
            data=stock_serialized.data,
            entity="Stock"
        )

    def update(self, request, pk=None):
        user_id = request.user.id
        logger.info(
            f"User {user_id} attempting to update stock ID: {pk}",
            extra={'action': 'update', 'user': user_id, 'stock_id': pk, 'data': request.data}
        )

        stock = self.get_stock_or_404(pk)
        serializer = self.get_serializer(stock, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)

        updated_stock = StockService.update_stock(
            instance=stock,
            validated_data=serializer.validated_data,
            user=request.user
        )

        logger.info(
            f"User {user_id} successfully updated stock ID: {updated_stock.id}",
            extra={
                'stock_id': updated_stock.id,
                'updated_fields': list(serializer.validated_data.keys()),
                'user': user_id
            }
        )

        return ResponseWrapper.updated(
            data=self.get_serializer(updated_stock).data,
            entity=f"Stock {updated_stock.id}",
            metadata={
                'updated_fields': list(serializer.validated_data.keys())
            }
        )

    def destroy(self, request, pk=None):
        stock = self.get_stock_or_404(pk)
        user_id = getattr(request.user, 'id', 'Anonymous')
        logger.info(f"User {user_id} is attempting to delete stock ID: {stock.id}.")

        stock_id = stock.id 
        StockService.delete_stock(stock)

        logger.info(f"Stock ID: {stock_id} deleted successfully by user {user_id}.")
        return ResponseWrapper.deleted(
            entity=f"Stock {stock_id}",
        )

    def get_stock_or_404(self, pk) -> Stock:
        """Helper method with logging for object retrieval"""
        try:
            obj = self.queryset.get(pk=pk)
            logger.debug(f"Successfully retrieved stock ID: {obj.id}")
            return obj
        except Stock.DoesNotExist:
            logger.error(f"Stock not found. ID: {pk}")
            raise NotFound("Stock not found")