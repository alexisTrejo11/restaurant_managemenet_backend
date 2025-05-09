from typing import Optional, List
from ...domain.entities.ingredient import Ingredient
from ...application.mapper.ingredient_mappers import IngredientMappers
from ..models.ingredient_model import IngredientModel

class DjangoIngredientRepository:
    def __init__(self):
        pass

    def save(self, ingredient: Ingredient) -> Ingredient:
        ingredient_model = IngredientMappers.domainToModel(ingredient)

        ingredient_model.save()

        return IngredientMappers.modelToDomain(ingredient_model)

    def get_all(self) -> List[Ingredient]:
        ingredients = IngredientModel.objects.get_queryset()
        return [IngredientMappers.modelToDomain(ingredient) for ingredient in ingredients]

    def get_by_id(self, ingredient_id: int) -> Optional[Ingredient]:
        try:
            IngredientModel.objects.get(id=ingredient_id)
        except IngredientModel.DoesNotExist:
            return None

    def delete(self, ingredient_id: int) -> None:
        ingredient = IngredientModel.objects.filter(id=ingredient_id).first()
        ingredient.delete()