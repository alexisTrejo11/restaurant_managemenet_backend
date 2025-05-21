from core.response.django_response import DjangoResponseWrapper
from ..serializers.table_serializer import TableSerializer
from rest_framework.viewsets import ViewSet
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.utils.permission import RoleBasedPermission
from ....application.use_case.table_command_use_cases import (
    CreateTableUseCase,
    UpdateTableUseCase,
    DeleteTableUseCase,
)
from ....application.use_case.table_query_use_cases import (
    GetAllTablesUseCase,
    GetTableByIdUseCase
)

from dependency_injector.wiring import Provide
from core.injector.table_container import TableContainer

class TableViews(ViewSet):
    def __init__(self, 
        get_table_by_id: GetTableByIdUseCase = Provide[TableContainer.get_table_by_id],
        get_all_tables: GetAllTablesUseCase = Provide[TableContainer.get_all_tables],
        create_table: CreateTableUseCase = Provide[TableContainer.create_table],
        delete_table: DeleteTableUseCase = Provide[TableContainer.delete_table],
        **kwargs):
        self.get_table_by_number = get_table_by_id
        self.get_all_tables = get_all_tables
        self.create_table = create_table 
        self.delete_table = delete_table
        super().__init__(**kwargs)

    """
    def get_permissions(self):
    if self.action == 'get_all_tables':
            return [RoleBasedPermission(['admin', 'staff', 'waiter'])]
    elif self.action in ['create_table', 'delete_table_by_number']:
            return [RoleBasedPermission(['admin'])]
    else: # get_table_by_number
        return [RoleBasedPermission(['admin', 'staff'])]
    """

    @swagger_auto_schema(
        operation_description="Fetch a table by its number",
        responses={
            200: TableSerializer,
            404: openapi.Response('Table not found', TableSerializer),
        }
    )
    def retrieve(self, request, pk):
        table_output_dto = self.get_table_by_number.execute(pk, raise_exception=True)

        return DjangoResponseWrapper.found(
            data=table_output_dto.to_dict(), 
            entity="Table",
            param="Number",
            value=pk,
        )
    
    @swagger_auto_schema(
        operation_description="Fetch all tables",
        responses={
            200: TableSerializer(many=True),
        }
    )
    def list(self, request):        
        table_dto_list = self.get_all_tables.execute()
        if not table_dto_list or len(table_dto_list) == 0:
            return DjangoResponseWrapper.success(
                data=[],
                message="Not Tables Found"
            )
        
        tables_dict = [dto.to_dict() for dto in table_dto_list]
        return DjangoResponseWrapper.found(
            data=tables_dict,
            entity='All Tables',
        )

    @swagger_auto_schema(
        operation_description="Create a new table",
        request_body=TableSerializer,
        responses={
            201: TableSerializer,
            400: openapi.Response('Invalid request or table already exists')
        }
    )
    def create(self, request):
        serializer = TableSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        table_dto = self.create_table.execute(serializer.validated_data)

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
    def destroy(self, request, pk):
        self.delete_table.execute(pk)
        return DjangoResponseWrapper.no_content(message='Table successfully deleted')
    