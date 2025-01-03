from restaurant.repository.stock_repository import StockRepository
from restaurant.services.domain.stock import Stock, StockTransaction
from restaurant.utils.result import Result
from typing import Optional
from restaurant.utils.exceptions import StockNotFoundError
from injector import inject
import logging

logger = logging.getLogger(__name__)

class StockService:
    @inject
    def __init__(self, stock_repository : StockRepository):
        self.stock_repository = stock_repository


    def validate_unique_stock_per_product(self, ingredient):
        stock = self.stock_repository.get_by_ingredient(ingredient)
        return stock == None


    def get_stock_by_id(self, stock_id) -> Optional[Stock]:
        return self.stock_repository.get_by_id(stock_id)


    def get_stock_by_ingredient(self, ingredient) -> Optional[Stock]:
        return self.stock_repository.get_by_ingredient(ingredient)


    def get_all_stocks_sort_by_last_transaction(self) -> list:
        return self.stock_repository.get_all()


    def init_stock(self, ingredient, serializer) -> Stock:
        new_stock = Stock(
            id=None,
            ingredient=ingredient, 
            optimal_stock_quantity=serializer.get('optimal_stock_quantity')
        )
        
        new_stock = self.stock_repository.create(new_stock)
        
        logger.info(f"Stock for ingredient {ingredient.name} created successfully with ID {new_stock.id}.")
        return new_stock


    def clear_stock(self, id) -> Stock:
        stock = self.stock_repository.get_by_id(id)
        if not stock:
            logger.warning(f"Stock with ID {id} not found.")
            raise StockNotFoundError(f"Stock with ID {id} not found")

        stock.clear()
        self.stock_repository.update(stock)
        
        logger.info(f"Stock with ID {id} cleared successfully.")
        return stock


    def add_transaction(self, stock: Stock, transaction: StockTransaction) -> Stock:
        stock.add_transaction(transaction)
        self.stock_repository.save_transaction(transaction)
        
        updated_stock = self.stock_repository.update(stock)
        
        logger.info(f"Transaction added to stock with ID {stock.id}. Transaction ID: {transaction.id}")
        return updated_stock


    def delete_stock_by_id(self, id) -> bool:
        deleted = self.stock_repository.delete(id)
        
        if deleted:
            logger.info(f"Stock with ID {id} deleted successfully.")
        else:
            logger.warning(f"Failed to delete stock with ID {id}.")
        
        return deleted

    def validate_transaction(self, stock: Stock, transaction: StockTransaction) -> Result:
        validation_map = stock.validate_transaction(transaction)
        if not validation_map["is_valid"]:
            return Result.error(validation_map["message"])

        return Result.success(None)



