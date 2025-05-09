from abc import ABC, abstractmethod
from core.repository.common_repository import CommonRepository
from ...domain.entities.stock import Stock
from typing import Optional

class StockRepository(CommonRepository[Stock]):
    @abstractmethod
    def get_by_ingredient(self, ingredient_id: int) -> Optional[Stock]:
        pass

    


