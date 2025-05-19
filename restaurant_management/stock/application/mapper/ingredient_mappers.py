from ...domain.entities.ingredient import Ingredient
from ...infrastructure.persistence.models.ingredient_model import IngredientModel
from ..dto.ingredient_response import IngredientResponse

class IngredientMappers:
    @staticmethod
    def dictToDomain(table_dict: dict) -> Ingredient:
        return Ingredient(
            name=table_dict.get('name'),
            unit=table_dict.get('unit'),
    )

    @staticmethod
    def modelToDomain(model: IngredientModel) -> Ingredient:
          return Ingredient(
            id=model.id,
            name=model.name,
            unit=model.unit,
            created_at=model.created_at,
            updated_at=model.updated_at,
     )
     
    @staticmethod
    def domainToModel(domain: Ingredient) -> IngredientModel:
        return IngredientModel(
            id=domain.id,
            name=domain.name,
            unit=domain.unit,
            created_at=domain.created_at,
            updated_at=domain.updated_at,
        )
     
    @staticmethod
    def domainToDTO(domain: Ingredient) -> IngredientResponse:
        return IngredientResponse(
            id=domain.id,
            name=domain.name,
            unit=domain.unit,
        )