from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from restaurant.utils.response import ApiResponse
from rest_framework.decorators import api_view
from restaurant.services.table_service import TableService
from rest_framework.exceptions import ValidationError
from restaurant.serializers import TableSerializer

@api_view(['POST'])
def create_table(request): 
    try:
        TableService.create_table(request.data)  
        
        return ApiResponse.created('Table successfully created')
    except ValidationError as e:        
        return ApiResponse.bad_request(e.detail)


@api_view(['GET'])
def get_table_by_number(request, table_number):
    table = TableService.get_table_by_number(table_number)

    if table is None:
        return ApiResponse.not_found(f'Table with number {table_number} not found.')
    
    table_data = TableSerializer(tables, many=True).data 
    return ApiResponse.ok(table_data, f'Table with number:{table_number} successfully fetched')

 
@api_view(['GET'])
def get_tables(request):
    tables = TableService.get_tables_sorted_by_number()

    table_data = TableSerializer(tables, many=True).data 
    return ApiResponse.ok(table_data, f'Tables(sorted by number) successfully fetched')


@api_view(['GET'])
def get_table_by_number(request, table_number):
    table = TableService.get_table_by_number(table_number)
    
    if table is None:
        return ApiResponse.not_found(f'Table with number {table_number} not found.')

    table_data = TableSerializer(table).data
    return ApiResponse.ok(table_data, f'Table with number:{table_number} successfully fetched')


@api_view(['DELETE'])
def delete_table_by_number(request, table_number):
    is_table_deleted = TableService.delete_table_by_number(table_number)
    
    if not is_table_deleted:
        return ApiResponse.not_found(f'Table with number {table_number} not found.')
    
    return ApiResponse.ok(f'Table with number {table_number} successfully deleted.')