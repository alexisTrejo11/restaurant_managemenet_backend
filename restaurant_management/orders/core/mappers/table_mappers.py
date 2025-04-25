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
            number=table.number,
            capacity=table.capacity,
            is_available=table.is_available,
            created_at=table.created_at,
            updated_at=table.updated_at,
        )

    @staticmethod
    def to_domain(dto: TableDTO) -> Table:
        """
        Maps a TableDTO to a Table domain entity.
        
        Args:
            dto (TableDTO): The TableDTO to map.
        
        Returns:
            Table: The corresponding Table domain entity.
        """
        return Table(
            number=dto.number,
            capacity=dto.capacity,
            is_available=dto.is_available,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )
