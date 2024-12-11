"""
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from restaurant.services.stock_service import StockService
from restaurant.services.ingredient_service import IngredientService
from restaurant.utils.result import Result
from restaurant.serializers import IngredientSerializer, StockInsertSerializer, StockSerializer, StockUpdateSerializer
from restaurant.utils.response import ApiResponse

@api_view(['GET'])
def get_stock_by_id(request, stock_id):
    stock_result = StockService.get_stock_by_id(stock_id)
    
    if stock_result.is_failure():
        return ApiResponse.not_found(stock_result.get_error_msg())
        
    stock_serializer = StockSerializer(stock_result.get_data())
    
    return ApiResponse.ok(stock_serializer, f'Stock with Id {stock_id} successfully fetched')


@api_view(['GET'])
def get_stock_by_ingredient_id(request, ingredient_id):
    # Validate existing ingredient
    ingredient = IngredientService.get_ingredient_by_id(ingredient_id)
    if ingredient is None:
        return ApiResponse.not_found(f'Can not create a stock with a ingredient that does not exists')

    # Retrieve stock by ingredient id
    stock_result = StockService.get_stock_by_ingredient_id(ingredient_id)
    if stock_result.is_failure():
        return ApiResponse.not_found(stock_result.get_error_msg())
    
    stock = stock_result.get_data()
    stock_data = StockSerializer(stock).data

    return ApiResponse.ok(stock_data, f'Stock with ingredient Id {ingredient_id} successfully fetched')


@api_view(['POST'])
def init_stock(request, ingredient_id):
    stock_serializer = StockInsertSerializer(data=request.data)

    # Validate the incoming data
    if not stock_serializer.is_valid():
        return ApiResponse.bad_request(stock_serializer.errors)
       
    optimal_quantity = stock_serializer.validated_data['optimal_quantity']

    # Validate existing ingredient
    ingredient_result = IngredientService.get_ingredient_entity_by_id(ingredient_id)
    if ingredient_result.is_failure():
        return ApiResponse.not_found(ingredient_result.get_error_msg())

    # Validate unique ingredient per stock
    ingredient_stock_validation = StockService.validate_stock_creation(ingredient_id)
    if ingredient_stock_validation.is_failure():
        return ApiResponse.bad_request(ingredient_stock_validation.get_error_msg())

    # Initialize stock
    stock = StockService.init_stock(ingredient_result.get_data(), optimal_quantity)
    stock_data = StockSerializer(stock).data
    
    return ApiResponse.created(stock, f'Stock with ingredient Id {ingredient_id} successfully initialized')


@api_view(['PUT'])
def update_stock_by_ingredient_id(request):
    stock_serializer = StockUpdateSerializer(data=request.data)
    
    if not stock_serializer.is_valid():
        return ApiResponse.bad_request(stock_serializer.errors)

    stock_result = StockService.update_stock(stock_serializer.validated_data)

    if stock_result.is_failure():
        return ApiResponse.bad_request(stock_result.get_error_msg())
    
    ingredient_id = stock_serializer.validated_data["ingredient_id"]

    return ApiResponse.ok(f'Stock with ingredient Id {ingredient_id} successfully updated')
  

@api_view(['DELETE'])
def delete_stock_by_ingredient_id(request, ingredient_id):
    delete_result = StockService.delete_stock_by_ingredient_id(ingredient_id)
    if delete_result.is_failure():
        return ApiResponse.not_found(f'Stock with ingredient Id {ingredient_id} not found')

    return ApiResponse.ok(f'Stock with ingredient Id {ingredient_id} successfully deleted')
"""