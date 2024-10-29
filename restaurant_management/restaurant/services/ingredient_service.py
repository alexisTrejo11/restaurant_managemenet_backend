from restaurant.models import Ingredient
from restaurant.serializers import IngredientSerializer
from rest_framework.exceptions import ValidationError

class IngredientService:
    @staticmethod
    def get_ingredient_by_id(ingredient_id):
        try:
            ingredient = Ingredient.objects.get(id=ingredient_id)
            
            serializer = IngredientSerializer(ingredient)
            return serializer.data
        except Ingredient.DoesNotExist:
            return None
    
    @staticmethod
    def get_ingredient_entity_by_id(ingredient_id):
        try:
            return Ingredient.objects.get(id=ingredient_id)
        
        except Ingredient.DoesNotExist:
            return None



    @staticmethod
    def get_ingredients():
        tables = Ingredient.objects.all().order_by('id')
        
        serializer = IngredientSerializer(tables, many=True)
        return serializer.data


    @staticmethod
    def create_ingredient(data):
        serializer = IngredientSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            raise ValidationError(serializer.errors) 


    @staticmethod
    def delete_ingredient(ingredient_id):
        try:
            ingredient = Ingredient.objects.get(id=ingredient_id)
            ingredient.delete()
            return True
        except Ingredient.DoesNotExist:
            return False
