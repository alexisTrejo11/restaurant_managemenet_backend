from restaurant.models import Ingredient
from rest_framework.exceptions import ValidationError
from restaurant.repository.ingredient_repository import IngredientRepository

class IngredientService:
    def __init__(self):
        self.ingredient_repository = IngredientRepository()


    def get_ingredient_by_id(self, ingredient_id) -> Ingredient:
        return self.ingredient_repository.get_by_id(ingredient_id)


    def get_all_ingredients(self) -> list:
        return self.ingredient_repository.get_all()

    def create_ingredient(self, data) -> Ingredient:
        ingredient = Ingredient(
            name=data.get('name'),
            unit=data.get('unit')
            )

        self.ingredient_repository.create(ingredient)

        return ingredient


    def delete_ingredient(self, ingredient_id):
        return self.ingredient_repository.delete(ingredient_id)
            
