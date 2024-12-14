from restaurant.repository.models.models import IngredientModel
from restaurant.services.domain.ingredient import Ingredient
from restaurant.repository.common_repository import CommonRepository
from typing import List, Optional
from restaurant.mappers.ingredient_mappers import IngredientMappers


class IngredientRepository(CommonRepository[Ingredient]):
    def __init__(self):
        self.ingredient_model = IngredientModel


    def get_all(self) -> List[Ingredient]:
        ingredient_models = self.ingredient_model.objects.all().order_by('id')
        ingredients = [
            IngredientMappers.modelToDomain(ingredient_model)
            for ingredient_model in ingredient_models
        ]
        return ingredients


    def get_by_id(self, ingredient_id: int) -> Optional[Ingredient]:
        ingredient_model = self.ingredient_model.objects.filter(id=ingredient_id).first()
        if ingredient_model:
            return IngredientMappers.modelToDomain(ingredient_model)
        return None
	

    def create(self, ingredient: Ingredient) -> Ingredient:
        new_ingredient = self.ingredient_model(
            name=ingredient.name,
            unit=ingredient.unit
        )
        new_ingredient.save()
        return ingredient


    def update(self, ingredient: Ingredient) -> Optional[Ingredient]:
        model = self.ingredient_model.objects.filter(id=ingredient.id).first()
        if not model:
            return None
        model.name = ingredient.name
        model.unit = ingredient.unit
        model.save()
        return ingredient


    def delete(self, ingredient_id: int) -> bool:
        deleted, _ = self.ingredient_model.objects.filter(id=ingredient_id).delete()
        return deleted > 0
