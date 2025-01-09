from restaurant.services.domain.ingredient import Ingredient
from restaurant.repository.ingredient_repository import IngredientRepository
from injector import inject
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

class IngredientService:
    @inject
    def __init__(self, ingredient_repository: IngredientRepository):
        self.ingredient_repository = ingredient_repository


    def get_ingredient_by_id(self, ingredient_id) -> Ingredient:
        cache_key = f'ingredient_{ingredient_id}'
        
        ingredient = cache.get(cache_key)
        if ingredient is None:
            ingredient = self.ingredient_repository.get_by_id(ingredient_id)
            cache.set(cache_key, ingredient, timeout=3600) 
        
        return ingredient


    def get_all_ingredients(self) -> list:
        cache_key = 'all_ingredients'
        ingredients = cache.get(cache_key)

        if ingredients is None:
            ingredients = self.ingredient_repository.get_all()
            cache.set(cache_key, ingredients, timeout=600)
        
        return ingredients


    def create_ingredient(self, data) -> Ingredient:
        ingredient = Ingredient(
            name=data.get('name'),
            unit=data.get('unit')
        )
        
        created_ingredient = self.ingredient_repository.create(ingredient)
        logger.info(f"Ingredient with ID {created_ingredient.id} created successfully.")
        
        return created_ingredient

    def delete_ingredient(self, ingredient_id):
        is_delete = self.ingredient_repository.delete(ingredient_id)
        
        if is_delete:
            logger.info(f"Ingredient with ID {ingredient_id} deleted successfully.")
        
        return is_delete
