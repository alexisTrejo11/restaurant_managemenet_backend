from core.repository.common_repository import CommonRepository
from abc import ABC, abstractmethod
from ...core.domain.entities.menu_item import MenuItem 
from typing import List

class MenuItemRepository(CommonRepository[MenuItem], ABC):
    """
    An abstract repository interface for managing MenuItem entities.
    
    Extends the CommonRepository with additional methods specific to MenuItem.
    """

    @abstractmethod
    def search(self, filter_params: dict) -> List[MenuItem]:
        """
        Search for MenuItem entities based on filter parameters.
        
        Args:
            filter_params (dict): A dictionary of key-value pairs representing search filters.
        
        Returns:
            List[MenuItem]: A list of MenuItem entities matching the filters.
        """
        pass