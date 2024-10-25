from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from restaurant.services.ingredient_service import IngredientService

@api_view(['GET'])
def get_ingredient_by_id(request, ingredient_id):
    ingredient = IngredientService.get_ingredient_by_id(ingredient_id)
    if ingredient is None:
        return Response({
            'message': f'Ingredient with ID {ingredient_id} not found' 
        }, status=status.HTTP_404_NOT_FOUND)
    
    return Response({
        'message': f'Ingredient with ID {ingredient_id} successfully fetched',
        'data': ingredient, 
    })

@api_view(['GET'])
def get_ingredients(request):
    ingredients = IngredientService.get_ingredients()
    return Response({
        'message': 'Ingredients successfully fetched',
        'data': ingredients, 
    })

@api_view(['POST'])
def create_ingredient(request):
    try:
        IngredientService.create_ingredient(request.data)
        return Response({
            'message': 'Ingredient successfully created',
        }, status=status.HTTP_201_CREATED)
    except ValidationError as e:        
        return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_ingredient_by_id(request, ingredient_id):
    is_deleted = IngredientService.delete_ingredient(ingredient_id)
    if not is_deleted:
        return Response({
            'message': f'Ingredient with ID {ingredient_id} not found' 
        }, status=status.HTTP_404_NOT_FOUND)
    
    return Response({
        'message': f'Ingredient with ID {ingredient_id} successfully deleted',
    })
