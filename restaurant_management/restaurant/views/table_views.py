from restaurant.utils.response import ApiResponse
from restaurant.serializers import TableSerializer, TableInsertSerializer
from rest_framework.viewsets import ViewSet
from restaurant.services.table_service import TableService
from restaurant.injector.app_module import AppModule
from injector import Injector
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from restaurant.utils.permission import RoleBasedPermission

container = Injector([AppModule()])

class TableViews(ViewSet):
    # Role Permissions
    def get_permissions(self):
        if self.action == 'get_all_tables':
             return [RoleBasedPermission(['admin', 'staff', 'waiter'])]
        elif self.action in ['create_table', 'delete_table_by_number']:
             return [RoleBasedPermission(['admin'])]
        else: # get_table_by_number
            return [RoleBasedPermission(['admin', 'staff'])]

    # Table Service injection
    def get_table_service(self):
        return container.get(TableService)

    @swagger_auto_schema(
        operation_description="Fetch a table by its number",
        responses={
            200: TableSerializer,
            404: openapi.Response('Table not found', TableSerializer),
        }
    )
    def get_table_by_number(self, request, number):
        table_service = self.get_table_service()

        table = table_service.get_table_by_number(number)
        if table is None:
            return ApiResponse.not_found('Table', 'number', number)
        
        table_data = TableSerializer(table).data
        return ApiResponse.created(table_data, f'Table with number {number} successfully fetched')

    @swagger_auto_schema(
        operation_description="Fetch all tables",
        responses={
            200: TableSerializer(many=True),
        }
    )
    def get_all_tables(self, request):
        table_service = self.get_table_service()
        
        tables = table_service.get_all_tables()
        
        table_data = TableSerializer(tables, many=True).data
        return ApiResponse.ok(table_data, 'All tables successfully fetched')

    @swagger_auto_schema(
        operation_description="Create a new table",
        request_body=TableInsertSerializer,
        responses={
            201: TableSerializer,
            400: openapi.Response('Invalid request or table already exists')
        }
    )
    def create_table(self, request):
        table_service = self.get_table_service()

        serializer = TableInsertSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse.bad_request(serializer.errors)

        is_number_unique = table_service.validate_unique_table_number(serializer.validated_data)
        if not is_number_unique:
            return ApiResponse.bad_request(f'Table already exists')

        table = table_service.create_table(serializer.validated_data)
        table_data = TableSerializer(table).data

        return ApiResponse.created(table_data, "Table successfully created")

    @swagger_auto_schema(
        operation_description="Delete a table by its number",
        responses={
            204: 'Table successfully deleted',
            404: openapi.Response('Table not found')
        }
    )
    def delete_table_by_number(self, request, number):
        table_service = self.get_table_service()

        is_table_deleted = table_service.delete_table(number)
        if not is_table_deleted:
            return ApiResponse.not_found(f'table', 'number', number)
        
        return ApiResponse.deleted('Table')
    