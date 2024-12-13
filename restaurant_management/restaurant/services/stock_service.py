from restaurant.repository.stock_repository import StockRepository
from restaurant.services.domain.stock import Stock, StockTransaction
from restaurant.utils.result import Result
from typing import List, Optional
from restaurant.utils.exceptions import StockNotFoundError

class StockService:
    def __init__(self):
        self.stock_repository = StockRepository()


    def validate_unique_stock_per_product(self, ingredient):
        stock = self.stock_repository.get_by_ingredient(ingredient)
        return stock == None


    def init_stock(self, ingredient, serializer) -> Stock:
        new_stock = Stock(
            id=None,
            ingredient=ingredient, 
            optimal_stock_quantity=serializer.get('optimal_stock_quantity')
        )
        
        new_stock = self.stock_repository.create(new_stock)

        return new_stock


    def get_stock_by_id(self, stock_id) -> Optional[Stock]:
        return self.stock_repository.get_by_id(stock_id)


    def get_stock_by_ingredient(self, ingredient) -> Optional[Stock]:
        return self.stock_repository.get_by_ingredient(ingredient)


    def get_all_stocks_sort_by_last_transaction(self) -> list:
        return self.stock_repository.get_all()


    def clear_stock(self, id) -> Stock:
        stock = self.stock_repository.get_by_id(id)
        if not stock:
            raise StockNotFoundError(f"Stock with ID {stock_id} not found")

        stock.clear()
        self.stock_repository.update(stock)

        return stock

    def validate_transaction(self, stock: Stock, transaction: StockTransaction) -> Result:
        validation_map = stock.validate_transaction(transaction)
        if not validation_map["is_valid"]:
            return Result.error(validation_map["message"])

        return Result.success(None)

    def add_transaction(self, stock: Stock, transaction: StockTransaction) -> Stock:
            stock.add_transaction(transaction)
            self.stock_repository.save_transaction(transaction)
            
            return self.stock_repository.update(stock)


    def delete_stock_by_id(self, id) -> bool:
        return self.stock_repository.delete(id)





