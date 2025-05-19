from typing import List
from injector import inject
from ..dto.ingredient_response import IngredientResponse
from ...domain.entities.ingredient import Ingredient
from ..mapper.ingredient_mappers import IngredientMappers
from ...application.repositories.ingredient_repository import IngredientRepository

class GetAllIngredientsUseCase:
    @inject
    def __init__(self, ingredient_repository: IngredientRepository):
        self.ingredient_repository = ingredient_repository 

    def execute(self) -> List[IngredientResponse]:
        ingredients = self.ingredient_repository.get_all()
        return [IngredientMappers.domainToDTO(ingredient) for ingredient in ingredients]

class GetIngredientsByIdUseCase:
    @inject
    def __init__(self, ingredient_repository: IngredientRepository):
        self.ingredient_repository = ingredient_repository 
    
    def execute(self, ingredient_id: int):
        ingredient = self.ingredient_repository.get_by_id(ingredient_id)
        if not ingredient:
            raise ValueError("Ingredient Not Found")

        return IngredientMappers.domainToDTO(ingredient)

class CreateIngredientUseCase:
    @inject
    def __init__(self, ingredient_repository: IngredientRepository):
        self.ingredient_repository = ingredient_repository 
    
    def execute(self, ingredient_data: dict):
        ingredient = IngredientMappers.dictToDomain(ingredient_data)

        self.ingredient_repository.save(ingredient)

        return IngredientMappers.domainToDTO(ingredient)
        

class UpdateIngredientUseCase:
    @inject
    def __init__(self, ingredient_repository: IngredientRepository):
        self.ingredient_repository = ingredient_repository 
    
    def execute(self, ingredient_data: dict):
        ingredient = IngredientMappers.dictToDomain(ingredient_data)
        ingredient.id = ingredient_data.get('id') if ingredient_data.get('id') else None

        self.ingredient_repository.save(ingredient)

        return IngredientMappers.domainToDTO(ingredient)


class DeleteIngredientUseCase:
    @inject
    def __init__(self, ingredient_repository: IngredientRepository):
        self.ingredient_repository = ingredient_repository 

    def execute(self, ingredient_id: int):
        ingredient = self.ingredient_repository.get_by_id(ingredient_id)
        if not ingredient:
            raise ValueError("Ingredient Not Found")

        self.ingredient_repository.delete(ingredient.id)