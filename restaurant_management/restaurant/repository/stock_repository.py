from restaurant.repository.common_repository import CommonRepository
from restaurant.services.domain.stock import Stock
from restaurant.repository.models.models import StockModel, StockTransactionModel

class StockRepository(CommonRepository[Stock]):
     def __init__(self):
          self.stock = StockModel


     def get_all(self):
          return self.stock.objects.all().order_by('number')


     def get_by_id(self, id):
          return self.stock.objects.filter(id=id).first()


     def create(self, table: Stock) -> Stock:
          return self.stock.objects.create(
               number=table.number,
               seats=table.seats,
               is_available=table.is_available
          )          


     def update(self, table: Stock) -> Stock:
          pass


     def delete(self, number) -> bool:
        deleted, _ = self.stock.objects.filter(number=number).delete()
        return deleted > 0
