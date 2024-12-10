from restaurant.models import Table 

class TableRepository:
     def __init__(self):
          self.table = Table

     def get_all(self):
          return self.table.objects.all().order_by('number')

     def get_by_number(self, number):
          return self.table.objects.filter(number=number).first()


     def create(self, table: Table):
          return self.table.objects.create(
               number=table.number,
               seats=table.seats,
               is_available=table.is_available
          )          

     def delete_by_number(self, number) -> bool:
        deleted, _ = self.table.objects.filter(number=number).delete()
        return deleted > 0