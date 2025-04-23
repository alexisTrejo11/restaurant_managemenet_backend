from restaurant.repository.common_repository import CommonRepository
from restaurant.services.domain.stock import Stock, StockTransaction
from restaurant.mappers.stock_mappers import StockMappers, StockTransactionMappers
from restaurant.models import StockModel, StockTransactionModel
from typing import List, Optional


class StockRepository(CommonRepository[Stock]):
     def __init__(self):
          self.stock = StockModel


     def get_all(self) -> List[Stock]:
          stock_model = self.stock.objects.all().order_by('updated_at')
          
          stocks = [StockMappers.modelToDomain(stock_model) for stock_model in stock_model]
          return stocks


     def get_by_id(self, id) -> Optional[Stock]:
          stock_model = self.stock.objects.filter(id=id).first()
          if stock_model is not None:
               return StockMappers.modelToDomain(stock_model)
               

     def get_by_ingredient(self, ingredient) -> Optional[Stock]:
          stock_model = self.stock.objects.filter(ingredient=ingredient.id).first()
          if stock_model:
               return StockMappers.modelToDomain(stock_model)


     def create(self, stock: Stock) -> Stock:
          stock_model = StockMappers.domainToModel(stock)

          stock_model.save()
          
          return StockMappers.modelToDomain(stock_model)
        

     def update(self, stock: Stock) -> Stock:
          stock_model = StockMappers.domainToModel(stock)
          
          stock_model.save()

          return StockMappers.modelToDomain(stock_model)


     def save_transaction(self, transaction : StockTransaction):
          transaction_model = StockTransactionMappers.domainToModel(transaction)
          
          transaction_model.save()


     def delete(self, id) -> bool:
        deleted, _ = self.stock.objects.filter(id=id).delete()
        return deleted > 0


