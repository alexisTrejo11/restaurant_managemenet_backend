from restaurant.utils.response import ApiResponse
from restaurant.serializers import TableSerializer, TableInsertSerializer
from rest_framework.views import APIView
from restaurant.services.table_service import TableService

table_service = TableService()

class GetTableByNumber(APIView):
    def get(self, request, table_number):
        table = table_service.get_table_by_number(table_number)
        if table is None:
            return ApiResponse.not_found(f'Table with number {table_number} not found')
        
        table_data = TableSerializer(table).data

        return ApiResponse.created(table_data, f'Table with number {table_number} succesfully fetched')


class GetAllTables(APIView):    
    def get(self, request):
        tables = table_service.get_all()
        table_data = TableSerializer(tables, many=True).data
        return ApiResponse.ok(table_data, 'All tables succesfully fetched')


class CreateTable(APIView):    
    def post(self, request):
        serializer = TableInsertSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse.bad_request(serializer.errors)

        is_number_unique = table_service.validate_unique_table_number(serializer.validated_data)
        if not is_number_unique:
            return ApiResponse.bad_request(f'Table already exsits')


        table = table_service.create_table(serializer.validated_data)
        table_data = TableSerializer(table).data

        return ApiResponse.created(table_data, "Table successfully created")



class DeleteTable(APIView): 
    def delete(self, request, table_number):
        is_table_deleted = table_service.delete_table(table_number)
        if not is_table_deleted:
            return ApiResponse.not_found(f'table', 'table number', table_number)
        
        return ApiResponse.deleted('Table')
