from restaurant.models import Ingredient
from rest_framework.exceptions import ValidationError
from restaurant.utils.result import Result

class IngredientService:
    @staticmethod
    def get_ingredient_by_id(ingredient_id):
        try:
            ingredient = Ingredient.objects.get(id=ingredient_id)
            return Result.success(ingredient)
        except Ingredient.DoesNotExist:
            return Result.error(f'Ingredient with ID {ingredient_id} not found')
    
    @staticmethod
    def get_ingredient_entity_by_id(ingredient_id):
        try:
            return Ingredient.objects.get(id=ingredient_id)
        
        except Ingredient.DoesNotExist:
            return None



    @staticmethod
    def get_all_ingredients():
        return Ingredient.objects.all().order_by('id')
        

    @staticmethod
    def create_ingredient(data):
        ingredient = Ingredient(
            name=data.get('name'),
            quantity=data.get('quantity'),
            unit=data.get('unit')
            )

        ingredient.save()

        return ingredient


    @staticmethod
    def delete_ingredient(ingredient_id):
        try:
            ingredient = Ingredient.objects.get(id=ingredient_id)
            ingredient.delete()
            
            return Result.success(None)
        except Ingredient.DoesNotExist:
            return Result.error(f'Ingredient with ID {ingredient_id} successfully deleted')
