from injector import inject
from ...core.domain.entities.table_entity import Table
from ...core.repositories.table_repository import TableRepository
from ...core.mappers.table_mappers import TableMapper
from ..dtos.table_dto import TableDTO

class CreateTableUseCase:
    """
    Use case for creating a new table.
    """
    @inject
    def __init__(self, table_repository: TableRepository):
        self.table_repository = table_repository

    def execute(self, validated_data: dict) -> TableDTO:
        """
        Create a new table and save it to the repository.
        
        Args:
            table (Table): The table entity to create.
        
        Returns:
            Table: The created table.
        """
        new_table = TableMapper.to_domain(validated_data)
        
        table_created = self.table_repository.save(new_table)
        
        return TableMapper.to_dto(table_created)


class UpdateTableUseCase:
    """
    Use case for updating an existing table.
    """
    @inject
    def __init__(self, table_repository: TableRepository):
        self.table_repository = table_repository

    def execute(self, table_update_data: dict) -> TableDTO:
        """
        Update an existing table in the repository.
        
        Args:
            table (Table): The table entity to update.
        
        Returns:
            Table: The updated table.
        """
        table = self.table_repository.get_by_id(table_update_data['id'], raise_expection=True)

        return self.table_repository.update(table)
    

class DeleteTableUseCase:
    """
    Use case for deleting a table.
    """
    @inject
    def __init__(self, table_repository: TableRepository):
        self.table_repository = table_repository

    def execute(self, number: int) -> None:
        """
        Delete a table from the repository.
        
        Args:
            number (int): The number (number act as ID) of the table to delete.
        
        Returns:
            bool: True if the table was deleted, False otherwise.
        """
        table = self.table_repository.get_by_id(number, raise_expection=True)

        self.table_repository.delete(table.number)


class SetTableAsAvailableUseCase:
    """
    Use case for setting a table as available.
    """
    @inject
    def __init__(self, table_repository: TableRepository):
        self.table_repository = table_repository

    def execute(self, number: int) -> None:
        """
        Set a table as available in the repository.
        
        Args:
            number (int): The number of the table to mark as available.
        """
        self.table_repository.set_as_available(number)


class SetTableAsUnavailableUseCase:
    """
    Use case for setting a table as unavailable.
    """
    @inject
    def __init__(self, table_repository: TableRepository):
        self.table_repository = table_repository

    def execute(self, number: int) -> None:
        """
        Set a table as unavailable in the repository.
        
        Args:
            number (int): The number of the table to mark as unavailable.
        """
        self.table_repository.set_as_unavailable(number)