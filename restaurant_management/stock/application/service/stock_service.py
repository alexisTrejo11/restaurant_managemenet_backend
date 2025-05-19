from ..repositories.stock_repository import StockRepository
from typing import Optional, List
from injector import inject
from ...domain.entities.stock import Stock
from ...domain.entities.ingredient import Ingredient
from ...domain.exceptions.stock_exceptions import *

class StockService:
    @inject
    def __init__(self, stock_repository: StockRepository):
        self.stock_repository = stock_repository

    def get_all_stocks(self) -> List[Stock]:
        return self.stock_repository.get_all()
    
    def get_stock_by_id(self, stock_id, raise_exception=False) -> Optional[Stock]:
        stock = self.stock_repository.get_by_id(stock_id)
        if not stock and raise_exception:
            raise StockNotFoundError(f"Stock con ID {stock_id} no encontrado") 
        return stock

    def get_stock_by_ingredient(self, ingredient : Ingredient, raise_exception=False) -> Optional[Stock]:
        stock = self.stock_repository.get_by_ingredient(ingredient.id)
        if not stock and raise_exception:
            raise StockNotFoundError(f"Stock con ID {ingredient.id} no encontrado") 
        return stock

    def create_stock(self, new_stock : Stock) -> Stock:
        if not self.validate_unique_stock_per_product(new_stock.ingredient):
            raise DuplicateStockError(f"Ya existe un stock para el ingrediente {new_stock.ingredient.name}")
        
        new_stock.validate_fields()

        return self.stock_repository.save(new_stock)

    def validate_unique_stock_per_product(self, ingredient) -> bool:
        return self.stock_repository.get_by_ingredient(ingredient) is None


    def clear_stock(self, stock_id) -> Stock:
        stock = self.get_stock_by_id(stock_id)
        stock.clear()
        return self.stock_repository.update(stock)
    
    def delete_stock(self, stock_id) -> Stock:
        stock = self.stock_repository.get_by_id(stock_id, raise_exception=True)

        self.stock_repository.delete(stock.id)