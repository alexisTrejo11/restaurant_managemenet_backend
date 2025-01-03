from restaurant.repository.models.models import TableModel 
from restaurant.services.domain.table import Table 
from restaurant.repository.common_repository import CommonRepository
from typing import List
from restaurant.mappers.table_mappers import TableMappers

class TableRepository(CommonRepository[TableModel]):
    def __init__(self):
        self.table = TableModel


    def get_all(self) -> List[Table]:
        model = self.table.objects.all().order_by('number')
        return TableMappers.to_domain(model)


    def get_by_id(self, number):
        model = self.table.objects.filter(number=number).first()
        return TableMappers.to_domain(model)


    def set_as_available(self, number):
        table = self.table.objects.filter(number=number).first()
        if table:
            table.is_available = True
            table.save()


    def set_as_unavailable(self, number):
        table = self.table.objects.filter(number=number).first()
        if table:
            table.is_available = False
            table.save()


    def create(self, table: Table) -> Table:
        model = self.table.objects.create(
            number=table.number,
            seats=table.seats,
            is_available=table.is_available
        )
        return TableMappers.to_domain(model)
   

    def update(self, table: Table) -> Table:
        pass

    def delete(self, number) -> bool:
        deleted, _ = self.table.objects.filter(number=number).delete()
        return deleted > 0