from rest_framework.exceptions import ValidationError
from restaurant.models import Table
from restaurant.repository.table_respository import TableRepository

class TableService:
    def __init__(self, table_repository : TableRepository):
        self.table_repository = table_repository


    def get_table_by_number(self, number : int) -> Table:
        return self.table_repository.get_by_number(number)


    def get_all(self) -> list:
        return self.table_repository.get_all()


    def create_table(self, validated_data) -> Table:
        new_table = Table(
            number=validated_data['number'],
            seats=validated_data['seats'],
            is_available=True
        )

        return self.table_repository.create(new_table)

        return new_table


    def delete_table_by_number(self, number) -> bool:
        return self.table_repository.delete_by_number(number)
