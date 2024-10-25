from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from restaurant.services.menu_service import MenuService
from rest_framework.exceptions import ValidationError

@api_view(['GET'])
def get_menu_by_id(request, menu_id):
    menu = MenuService.get_menu_by_id(menu_id)
    if menu is None:
        return Response({
            'message': f'menu with id {menu_id} not found.'
        }, status=status.HTTP_404_NOT_FOUND)
        
    return Response({
        'message': f'menu with id:{menu_id} successfully fetched',
        'data': menu
    })


@api_view(['GET'])
def get_menus_by_category(request, category):
    menus = MenuService.get_menus_by_category(category)
    if menus is None:
        return Response({
            'message': f'Category with name {category} not found.'
        }, status=status.HTTP_404_NOT_FOUND)

    return Response({
        'message': f'Menus with category {category} successfully fetched',
        'data': menus
    })


@api_view(['POST'])
def create_menu(request):
    try:
        MenuService.create_menu(request.data)  
        
        return Response({
            'message': 'menu successfully created',
        }, status=status.HTTP_201_CREATED)
    except ValidationError as e:        
        return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST) 


@api_view(['DELETE'])
def delete_menu_by_id(request, menu_id):
    is_menu_deleted = MenuService.delete_menu_by_id(menu_id)
    if not is_menu_deleted:
        return Response({
            'message': f'menu with id {menu_id} not found.'
        }, status=status.HTTP_404_NOT_FOUND)

    return Response({
        'message': f'menu with id {menu_id} successfully deleted.'
    }, status=status.HTTP_200_OK)
