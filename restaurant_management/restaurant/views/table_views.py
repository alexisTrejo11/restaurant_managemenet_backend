from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from restaurant.services.table_service import TableService
from rest_framework.exceptions import ValidationError

@api_view(['POST'])
def create_table(request):
    if request.method == 'POST':  
        try:
            TableService.create_table(request.data)  
            
            return Response({
                'message': 'Table successfully created',
            }, status=status.HTTP_201_CREATED)
        except ValidationError as e:        
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST) 


@api_view(['GET'])
def get_table_by_number(request, table_number):
    table = TableService.get_table_by_number(table_number)
    if table is None:
        return Response({
            'message': f'Table with number {table_number} not found.'
        }, status=status.HTTP_404_NOT_FOUND)
        
    return Response({
        'message': f'Table with number:{table_number} successfully fetched',
        'data': table
    })


@api_view(['GET'])
def get_tables(request):
    tables = TableService.get_tables_sorted_by_number()
    return Response({
        'message': f'Tables(sorted by number) successfully fetched',
        'data': tables
    })


@api_view(['GET'])
def get_table_by_number(request, table_number):
    table = TableService.get_table_by_number(table_number)
    if table is None:
        return Response({
            'message': f'Table with number {table_number} not found.'
        }, status=status.HTTP_404_NOT_FOUND)
        
    return Response({
        'message': f'Table with number:{table_number} successfully fetched',
        'data': table
    })


@api_view(['DELETE'])
def delete_table_by_number(request, table_number):
    is_table_deleted = TableService.delete_table_by_number(table_number)
    if not is_table_deleted:
        return Response({
            'message': f'Table with number {table_number} not found.'
        }, status=status.HTTP_404_NOT_FOUND)

    return Response({
        'message': f'Table with number {table_number} successfully deleted.'
    }, status=status.HTTP_200_OK)