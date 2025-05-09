from abc import abstractmethod
from typing import Optional, List
from ...domain.entities.ingredient import Ingredient

class IngredientRepository:
    def __init__(self):
        pass

    @abstractmethod
    def save(self, ingredient: Ingredient) -> Ingredient:
        pass

    @abstractmethod
    def get_all(self) -> List[Ingredient]:
        pass

    @abstractmethod
    def get_by_id(self, ingredient_id: int) -> Optional[Ingredient]:
        pass

    @abstractmethod
    def delete(self, ingredient_id: int) -> None:
        pass