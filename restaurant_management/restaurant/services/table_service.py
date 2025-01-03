from restaurant.services.domain.table import Table
from restaurant.repository.table_respository import TableRepository
from injector import inject
import logging

logger = logging.getLogger(__name__)


class TableService:
    @inject
    def __init__(self, table_repository: TableRepository):
        self.table_repository = table_repository


    def get_table_by_number(self, number : int) -> Table:
        return self.table_repository.get_by_id(number)


    def get_all_tables(self) -> list:
        return self.table_repository.get_all()


    def validate_unique_table_number(self, validated_data) -> bool:
        exisiting_table = self.table_repository.get_by_id(number= validated_data['number'])
        
        return exisiting_table is None


    def create_table(self, validated_data) -> Table:
        new_table = Table(
            number=validated_data['number'],
            seats=validated_data['seats'],
            is_available=True
        )

        created_table = self.table_repository.create(new_table)
        
        logger.info(f"Table with number {created_table.number} and {created_table.seats} seats created successfully.")
        return created_table


    def delete_table(self, number) -> bool:
        deleted = self.table_repository.delete(number)
        
        if deleted:
            logger.info(f"Table with number {number} deleted successfully.")
        else:
            logger.warning(f"Failed to delete table with number {number}.")
        
        return deleted