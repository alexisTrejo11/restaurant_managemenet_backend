from injector import inject
from typing import List, Optional
from ...core.domain.entities.table_entity import Table
from ...core.repositories.table_repository import TableRepository
from ...core.mappers.table_mappers import TableMapper
from ..dtos.table_dto import TableDTO

class GetAllTablesUseCase:
    """
    Use case for retrieving all tables.
    """
    @inject
    def __init__(self, table_repository: TableRepository):
        self.table_repository = table_repository

    def execute(self) -> List[TableDTO]:
        """
        Retrieve all tables from the repository.
        
        Returns:
            List[Table]: A list of all tables.
        """
        table_entity_list = self.table_repository.get_all()

        return [TableMapper.to_dto(entity) for entity in table_entity_list]

class GetTableByIdUseCase:
    """
    Use case for retrieving a table by its number.
    """
    @inject
    def __init__(self, table_repository: TableRepository):
        self.table_repository = table_repository

    def execute(self, id: int, raise_exception=False) -> Optional[TableDTO]:
        """
        Retrieve a table by its id.
        
        Args:
            id (int): The id of the table to retrieve.
            raise_excpetion (bool: False as default): The id of the table to retrieve.

        Returns:
            Optional[Table]: The retrieved table, or None if not found.
        """
        table_entity = self.table_repository.get_by_id(id, raise_exception=raise_exception)
        if not table_entity:
            return None
        
        return TableMapper.to_dto(table_entity)
