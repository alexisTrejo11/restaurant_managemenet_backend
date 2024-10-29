from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from restaurant.services.stock_service import StockService
from restaurant.services.ingredient_service import IngredientService
from restaurant.utils.result import Result
from restaurant.serializers import IngredientSerializer, StockInsertSerializer, StockSerializer, StockUpdateSerializer
from datetime import datetime
from restaurant.dtos.stock_dtos import StockUpdateDTO


@api_view(['GET'])
def get_stock_by_id(request, stock_id):
    stock_result = StockService.get_stock_by_id(stock_id)
    if stock_result.is_failure():
        return Response({
            'data': None,
            'message': stock_result.get_error_msg(),
            'time_stamp': datetime.now(),
        }, status=status.HTTP_404_NOT_FOUND)

    stock_serializer = StockSerializer(stock_result.get_data())
    return Response({
        'data': stock_serializer.data,
        'message': f'Stock with Id {stock_id} successfully fetched',
        'time_stamp': datetime.now(),
    })

@api_view(['GET'])
def get_stock_by_ingredient_id(request, ingredient_id):
    # Validate existing ingredient
    ingredient = IngredientService.get_ingredient_by_id(ingredient_id)
    if ingredient is None:
        return Response({
            'data': None,
            'message': f'Can not create a stock with a ingredient that does not exists',
            'time_stamp': datetime.now(),
        }, status=status.HTTP_404_NOT_FOUND)

    # Retrieve stock by ingredient id
    stock_result = StockService.get_stock_by_ingredient_id(ingredient_id)
    
    if stock_result.is_failure():
        return Response({
            'data': None,
            'message': stock_result.get_error_msg(),
            'time_stamp': datetime.now(),
        }, status=status.HTTP_404_NOT_FOUND)
    
    stock = stock_result.get_data()
    stock_data = StockSerializer(stock).data

    return Response({
        'data': stock_data,
        'message': f'Stock with ingredient Id {ingredient_id} successfully fetched',
        'time_stamp': datetime.now(),
    })

@api_view(['POST'])
def init_stock(request, ingredient_id):
    stock_serializer = StockInsertSerializer(data=request.data)

    # Validate the incoming data
    if not stock_serializer.is_valid():
        return Response({
            'data': None,
            'message': stock_serializer.errors,
            'time_stamp': datetime.now(),
        }, status=status.HTTP_400_BAD_REQUEST)

    optimal_quantity = stock_serializer.validated_data['optimal_quantity']

    # Validate existing ingredient
    ingredient_result = IngredientService.get_ingredient_entity_by_id(ingredient_id)
    if ingredient_result.is_failure():
        return Response({
            'data': None,
            'message': ingredient_result.get_error_msg(),
            'time_stamp': datetime.now(),
        }, status=status.HTTP_404_NOT_FOUND)

    ingredient = ingredient_result.get_data()

    # Validate unique ingredient per stock
    ingredient_stock_validation = StockService.validate_stock_creation(ingredient_id)
    if ingredient_stock_validation.is_failure():
        return Response({
            'data': None,
            'message': ingredient_stock_validation.get_error_msg(),
            'time_stamp': datetime.now(),
        }, status=status.HTTP_400_BAD_REQUEST)

    # Initialize stock
    stock = StockService.init_stock(ingredient, optimal_quantity)
    
    return Response({
        'data': stock,
        'message': f'Stock with ingredient Id {ingredient_id} successfully initialized',
        'time_stamp': datetime.now(),
    }, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def update_stock_by_ingredient_id(request):
    stock_serializer = StockUpdateSerializer(data=request.data)
    
    if not stock_serializer.is_valid():
        return Response({
            'data': None,
            'message': stock_serializer.errors,
            'time_stamp': datetime.now(),
        }, status=status.HTTP_400_BAD_REQUEST)

    stock_result = StockService.update_stock(stock_serializer.validated_data)

    if stock_result.is_failure():
        return Response({
            'data': None,
            'message': stock_result.get_error_msg(),
            'time_stamp': datetime.now(),
        }, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        'data': None,
        'message': f'Stock with ingredient Id {stock_serializer.validated_data["ingredient_id"]} successfully updated',
        'time_stamp': datetime.now(),
    })


@api_view(['DELETE'])
def delete_stock_by_ingredient_id(request, ingredient_id):
    delete_result = StockService.delete_stock_by_ingredient_id(ingredient_id)
    if delete_result.is_failure():
        return Response({
            'data': None,
            'message': f'Stock with ingredient Id {ingredient_id} not found',
            'time_stamp': datetime.now(),
        }, status=status.HTTP_404_NOT_FOUND)

    return Response({
        'data': None,
        'message': f'Stock with ingredient Id {ingredient_id} successfully deleted',
        'time_stamp': datetime.now(),
    }, status=status.HTTP_204_NO_CONTENT)
