from django.shortcuts import render
from rest_framework import status

from restaurant.utils.response import ApiResponse
from rest_framework.decorators import api_view
from rest_framework.decorators import action
from rest_framework.response import Response
from restaurant.models import Table
from rest_framework.exceptions import ValidationError
from restaurant.container import Container
from restaurant.serializers import TableSerializer, TableInsertSerializer

container = Container()

@api_view(['GET'])
def get_table_by_number(request, table_number):
    table_service = container.table_service()

    table = table_service.get_table_by_number(table_number)
    if table is None:
        return ApiResponse.not_found(f'Table with number {table_number} not found')
    
    table_data = TableSerializer(table).data

    return ApiResponse.created(f'Table with number succesfully created' ,table_data)

    
@api_view(['GET'])
def get_all_tables(request):
    table_service = container.table_service()

    tables = table_service.get_all()
    table_data = TableSerializer(tables, many=True).data
    return ApiResponse.ok(table_data, 'All tables succesfully fetched')


@api_view(['POST'])
def create_table(self, request):
    table_service = container.table_service()

    serializer = TableInsertSerializer(data=request.data)
    if not serializer.is_valid():
        return ApiResponse.bad_request(serializer.errors)

    table = table_service.create_table(serializer.validated_data)
    return ApiResponse.created("Table successfully created",
    data={"id": table.id, "number": table.number},
    )

@api_view(['DELETE'])
def delete_table_by_number(request, table_number):
    table_service = container.table_service()

    is_table_deleted = table_service.delete_table_by_number(table_number)
    if not is_table_deleted:
        return ApiResponse.not_found(f'Table with number {table_number} not found.')
    
    return ApiResponse.ok(None, f'Table with number {table_number} successfully deleted.')