from rest_framework.decorators import api_view
from restaurant.utils.response import ApiResponse
from restaurant.serializers import IngredientSerializer, IngredientInsertSerializer
from restaurant.services.ingredient_service import IngredientService
from django.views.decorators.http import require_http_methods
from rest_framework.views import APIView

ingredient_service = IngredientService()

class GetIngredientById(APIView):
    def get(self, request, ingredient_id):
        ingredient = ingredient_service.get_ingredient_by_id(ingredient_id)
        if ingredient is None:
            return ApiResponse.not_found('ingredient', 'ID', ingredient_id)
        
        ingredient_data = IngredientSerializer(ingredient).data

        return ApiResponse.found(ingredient_data, 'Ingredient', 'ID', ingredient_id)


class GetAllIngredients(APIView):
    def get(self, request):
        ingredients = ingredient_service.get_all_ingredients()
        ingrents_data = IngredientSerializer(ingredients, many=True).data

        return ApiResponse.ok(ingrents_data, 'Ingredients successfully fetched')


class CreateIngredient(APIView):
    def post(self, request):
        ingredient_serializer = IngredientInsertSerializer(data=request.data)
        if not ingredient_serializer.is_valid():
            return ApiResponse.bad_request(serializer.errors)
            
        ingredient = ingredient_service.create_ingredient(request.data)
        ingrents_data = IngredientSerializer(ingredient).data

        return ApiResponse.created(ingrents_data, 'Ingredient successfully created')


class DeleteIngredient(APIView):
    def delete(self, request, ingredient_id):
        is_deleted = ingredient_service.delete_ingredient(ingredient_id)
        if not is_deleted:
            return ApiResponse.not_found('Ingredient', 'ID', ingredient_id)
        
        return ApiResponse.ok(None, f'Ingredient with ID {ingredient_id} successfully deleted')
