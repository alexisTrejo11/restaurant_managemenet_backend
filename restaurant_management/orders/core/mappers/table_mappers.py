from typing import List
from ..domain.entities.table_entity import Table
from ...application.dtos.table_dto import TableDTO

class TableMapper:
    """
    Mapper class for converting between Table domain entities and TableDTOs.
    """

    @staticmethod
    def to_dto(table: Table) -> TableDTO:
        """
        Maps a Table domain entity to a TableDTO.
        
        Args:
            table (Table): The Table domain entity to map.
        
        Returns:
            TableDTO: The corresponding TableDTO.
        """
        return TableDTO(
            id=table.id,
            capacity=table.capacity,
            is_available=table.is_available,
            created_at=table.created_at,
            updated_at=table.updated_at,
        )

    @staticmethod
    def dict_to_domain(dto: dict) -> Table:
        """
        Maps a TableDTO to a Table domain entity.
        
        Args:
            dto (TableDTO): The TableDTO to map.
        
        Returns:
            Table: The corresponding Table domain entity.
        """
        return Table(
            id=dto.get('id'),
            capacity=dto.get('capacity'),
            is_available=True,
        )
    

    @staticmethod
    def model_to_domain(model) -> Table:
        """
        Maps a TableDTO to a Table domain entity.
        
        Args:
            dto (TableDTO): The TableDTO to map.
        
        Returns:
            Table: The corresponding Table domain entity.
        """
        return Table(
            id=model.id,
            capacity=model.capacity,
            is_available=model.is_available,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
