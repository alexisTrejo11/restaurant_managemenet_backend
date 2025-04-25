from core.response.django_response import DjangoResponseWrapper
from restaurant.serializers import TableSerializer, TableInsertSerializer
from rest_framework.viewsets import ViewSet
from core.injector.app_module import AppModule
from injector import Injector
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.utils.permission import RoleBasedPermission
from ....application.use_case.table_command_use_cases import (
    CreateTableUseCase,
    UpdateTableUseCase,
    DeleteTableUseCase,
    SetTableAsAvailableUseCase,
    SetTableAsUnavailableUseCase,
)
from ....application.use_case.table_query_use_cases import (
    GetAllTablesUseCase,
    GetTableByIdUseCase
)

container = Injector([AppModule()])

class TableViews(ViewSet):
    def __init__(self, **kwargs):
        self.get_table_by_number_use_case = GetTableByIdUseCase()
        self.get_all_tables_use_case = GetAllTablesUseCase()
        self.create_table_use_case = CreateTableUseCase()
        self.update_table_use_case = UpdateTableUseCase()
        self.set_as_available_table_use_case = SetTableAsAvailableUseCase()
        self.set_as_unavailable_table_use_case = SetTableAsUnavailableUseCase()
        self.delete_table_use_case = DeleteTableUseCase()
        super().__init__(**kwargs)

    def get_permissions(self):
        if self.action == 'get_all_tables':
             return [RoleBasedPermission(['admin', 'staff', 'waiter'])]
        elif self.action in ['create_table', 'delete_table_by_number']:
             return [RoleBasedPermission(['admin'])]
        else: # get_table_by_number
            return [RoleBasedPermission(['admin', 'staff'])]

    @swagger_auto_schema(
        operation_description="Fetch a table by its number",
        responses={
            200: TableSerializer,
            404: openapi.Response('Table not found', TableSerializer),
        }
    )
    def get_table_by_number(self, request, number):
        table_output_dto = self.get_table_by_number_use_case.execute(number, raise_exception=True)

        return DjangoResponseWrapper.found(
            data=table_output_dto.to_dict(), 
            entity="Table",
            param="Number",
            value=number,
        )
    
    @swagger_auto_schema(
        operation_description="Fetch all tables",
        responses={
            200: TableSerializer(many=True),
        }
    )
    def get_all_tables(self, request):        
        table_dto_list = self.get_all_tables_use_case.execute()
        
        tables_dict = [dto.to_dict() for dto in table_dto_list]
        return DjangoResponseWrapper.found(
            data=tables_dict,
            entity='All Tables',
        )

    @swagger_auto_schema(
        operation_description="Create a new table",
        request_body=TableInsertSerializer,
        responses={
            201: TableSerializer,
            400: openapi.Response('Invalid request or table already exists')
        }
    )
    def create_table(self, request):
        serializer = TableInsertSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        table_dto = self.create_table_use_case.execute(**serializer.validated_data)

        return DjangoResponseWrapper.created(
            data=table_dto.to_dict(), 
            entity='Table'
        )

    @swagger_auto_schema(
        operation_description="Delete a table by its number",
        responses={
            204: 'Table successfully deleted',
            404: openapi.Response('Table not found')
        }
    )
    def delete_table_by_number(self, request, number):
        self.delete_table_use_case.execute(number)
        return DjangoResponseWrapper.no_content(message='Table successfully deleted')
    