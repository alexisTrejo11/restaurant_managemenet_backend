from restaurant.repository.models.models import TableModel 
from restaurant.services.domain.table import Table 
from restaurant.repository.common_repository import CommonRepository

class TableRepository(CommonRepository[Table]):
     def __init__(self):
          self.table = TableModel


     def get_all(self):
          return self.table.objects.all().order_by('number')


     def get_by_id(self, number):
          return self.table.objects.filter(number=number).first()


     def create(self, table: Table) -> Table:
          return self.table.objects.create(
               number=table.number,
               seats=table.seats,
               is_available=table.is_available
          )          

     def update(self, table: Table) -> Table:
          pass

     def delete(self, number) -> bool:
        deleted, _ = self.table.objects.filter(number=number).delete()
        return deleted > 0