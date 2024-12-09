from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from restaurant.services.ingredient_service import IngredientService
from restaurant.utils.result import Result
from restaurant.utils.response import ApiResponse
from restaurant.serializers import IngredientSerializer


@api_view(['GET'])
def get_ingredient_by_id(request, ingredient_id):
    ingredient_result = IngredientService.get_ingredient_by_id(ingredient_id)
    
    if ingredient_result.is_failure():
        return ApiResponse.not_found(ingredient_result.get_error_msg())
    
    ingredient_data = IngredientSerializer(ingredient_result.get_data()).data

    return ApiResponse.found(ingredient_data, 'Ingredient', 'ID', ingredient_id)

@api_view(['GET'])
def get_all_ingredients(request):
    ingredients = IngredientService.get_all_ingredients()
    ingrents_data = IngredientSerializer(ingredients, many=True).data

    return ApiResponse.ok(ingrents_data, 'Ingredients successfully fetched')


@api_view(['POST'])
def create_ingredient(request):
    ingredient_serializer = IngredientSerializer(data=request.data)

    if not ingredient_serializer.is_valid():
        return ApiResponse.bad_request(serializer.errors)
         
    IngredientService.create_ingredient(request.data)

    return ApiResponse.created(None, 'Ingredient successfully created')


@api_view(['DELETE'])
def delete_ingredient_by_id(request, ingredient_id):
    delete_result = IngredientService.delete_ingredient(ingredient_id)
    
    if delete_result.is_failure():
        return ApiResponse.not_found(delete_result.get_error_msg())
    
    return ApiResponse.ok(None, f'Ingredient with ID {ingredient_id} successfully deleted')
