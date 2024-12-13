from restaurant.services.domain.ingredient import Ingredient
from restaurant.repository.models.models import IngredientModel


class IngredientMappers:
     @staticmethod
     def modelToDomain(model: IngredientModel) -> Ingredient:
          return Ingredient(
            id=model.id,
            name=model.name,
            unit=model.unit,
     )
     
     @staticmethod
     def domainToModel(domain: Ingredient) -> IngredientModel:
        return IngredientModel(
            id=domain.id,
            name=domain.name,
            unit=domain.unit,
        )