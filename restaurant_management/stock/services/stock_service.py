from datetime import datetime, timedelta
from django.db import transaction
from ..models import Stock, StockTransaction as StockTransactionModel
from ..exceptions.stock_exceptions import InvalidStockFieldError
from ..serializers import StockTransactionSerializer
import logging


logger = logging.getLogger(__name__)

class StockService:
    """
    Service for handling inventory business logic.
    """
    MAX_STOCK_LIMIT = 1000
    MIN_STOCK_LIMIT = 0
    
    @staticmethod
    def validate_stock_quantity(total_stock: int, optimal_stock: int) -> None:
        """Validate the stock quantities"""
        if not (StockService.MIN_STOCK_LIMIT <= total_stock <= StockService.MAX_STOCK_LIMIT):
            raise InvalidStockFieldError(f"The total stock must be within the range ({StockService.MIN_STOCK_LIMIT}, {StockService.MAX_STOCK_LIMIT})")
        if not (StockService.MIN_STOCK_LIMIT <= optimal_stock <= StockService.MAX_STOCK_LIMIT):
            raise InvalidStockFieldError(f"The optimal stock must be within the range ({StockService.MIN_STOCK_LIMIT}, {StockService.MAX_STOCK_LIMIT})")

    @classmethod
    def create_stock(cls, ingredient_id: int, optimal_quantity: int, initial_stock: int = 0) -> Stock:
        """Creates a new stock record"""
        cls.validate_stock_quantity(initial_stock, optimal_quantity)
        
        return Stock.objects.create(
            ingredient_id=ingredient_id,
            total_stock=initial_stock,
            optimal_stock_quantity=optimal_quantity
        )

    

    @classmethod
    def get_current_stock(cls, ingredient_id: int) -> int:
        """Gets the current stock of an ingredient"""
        try:
            stock = Stock.objects.get(ingredient_id=ingredient_id)
            return stock.total_stock
        except Stock.DoesNotExist:
            return 0

    @classmethod
    def get_stock_history(cls, stock_id: int, days: int = 30):
        """Gets the transaction history"""
        cutoff_date = datetime.now() - timedelta(days=days)
        return StockTransactionModel.objects.filter(
            stock_id=stock_id,
            date__gte=cutoff_date
        ).order_by('-date')


    @classmethod
    def delete_stock(cls, stock: Stock) -> int:
        try:
            with transaction.atomic():
                stock.delete()
        except Exception as e:
            logger.error(f"Error deleting table ID {stock.id}: {e}", exc_info=True)
            raise
