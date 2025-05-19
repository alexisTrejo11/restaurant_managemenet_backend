from ....domain.entities.stock import Stock, StockTransaction
from ....application.mapper.stock_mappers import StockMappers, StockTransactionMappers
from ..models.stock_model import StockModel, StockTransactionModel
from typing import List, Optional
from ....application.repositories.stock_repository import StockRepository

class DjangoStockRepository(StockRepository):
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


     def save(self, stock: Stock) -> Optional[Stock]:
          stock_model = StockMappers.domainToModel(stock)
          if not stock.id:
               return self._create(stock_model)
          else:
               return self._update(stock_model)

     def _create(self, stock: StockModel) -> Stock:
          stock.save()
          
          return StockMappers.modelToDomain(stock)
        
     def _update(self, stock: StockModel) -> Stock:
          stock_model = StockMappers.domainToModel(stock)
          
          stock_model.save()

          return StockMappers.modelToDomain(stock_model)
     
     def delete(self, id) -> bool:
        deleted, _ = self.stock.objects.filter(id=id).delete()
        return deleted > 0


