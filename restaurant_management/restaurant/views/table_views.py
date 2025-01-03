from restaurant.utils.response import ApiResponse
from restaurant.serializers import TableSerializer, TableInsertSerializer
from rest_framework.viewsets import ViewSet
from restaurant.services.table_service import TableService
from restaurant.injector.app_module import AppModule
from injector import Injector

container = Injector([AppModule()])

class TableViews(ViewSet):
    def get_table_service(self):
        return container.get(TableService)

    def get_table_by_number(self, request, number):
        table_service = self.get_table_service()

        table = table_service.get_table_by_number(number)
        if table is None:
            return ApiResponse.not_found('Table', 'number', number)
        
        table_data = TableSerializer(table).data

        return ApiResponse.created(table_data, f'Table with number {number} succesfully fetched')


    def get_all_tables(self, request):
        table_service = self.get_table_service()

        tables = table_service.get_all_tables()
        table_data = TableSerializer(tables, many=True).data
        return ApiResponse.ok(table_data, 'All tables succesfully fetched')


    def create_table(self, request):
        table_service = self.get_table_service()

        serializer = TableInsertSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse.bad_request(serializer.errors)

        is_number_unique = table_service.validate_unique_table_number(serializer.validated_data)
        if not is_number_unique:
            return ApiResponse.bad_request(f'Table already exsits')


        table = table_service.create_table(serializer.validated_data)
        table_data = TableSerializer(table).data

        return ApiResponse.created(table_data, "Table successfully created")


    def delete_table_by_number(self, request, number):
        table_service = self.get_table_service()

        is_table_deleted = table_service.delete_table(number)
        if not is_table_deleted:
            return ApiResponse.not_found(f'table', 'number', number)
        
        return ApiResponse.deleted('Table')
