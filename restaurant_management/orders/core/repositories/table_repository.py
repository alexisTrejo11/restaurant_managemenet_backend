from abc import abstractmethod, ABC
from typing import Optional
from ...core.domain.entities.table_entity import Table
from core.repository.common_repository import CommonRepository

class TableRepository(CommonRepository[Table], ABC):
    """
    An abstract repository interface for managing Table entities.
    
    Extends the CommonRepository with additional methods specific to Table.
    """

    @abstractmethod
    def set_as_available(self, number: int) -> None:
        """
        Set a table as available in the repository.
        
        Args:
            number (int): The number of the table to mark as available.
        """
        pass

    @abstractmethod
    def set_as_unavailable(self, number: int) -> None:
        """
        Set a table as unavailable in the repository.
        
        Args:
            number (int): The number of the table to mark as unavailable.
        """
        pass