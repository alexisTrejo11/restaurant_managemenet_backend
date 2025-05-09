from rest_framework.viewsets import ViewSet
from core.response.django_response import DjangoResponseWrapper
from ...application.mapper.stock_mappers import StockMappers
from ...serializers import StockInsertSerializer, StockSerializer, StockTransactionInsertSerializer
from core.injector.app_module import AppModule
from injector import Injector
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from ...application.use_case.stock_command_use_case import (
    CreateStockUseCase,
    UpdateStockUseCase,
    DeleteStockUseCase

) 

container = Injector([AppModule()])

class StockCommandViews(ViewSet):
    def __init__(self, **kwargs):
        self.init_stock_use_case = container.get(CreateStockUseCase)
        self.update_stock_use_case = container.get(UpdateStockUseCase)
        self.delete_stock_use_case = container.get(DeleteStockUseCase)
        super().__init__(**kwargs)

    permission_classes = [IsAuthenticated()]
    
    @swagger_auto_schema(
        operation_description="Initialize stock for an ingredient",
        request_body=StockInsertSerializer,
        responses={
            200: StockSerializer,
            400: "Invalid data or Ingredient not found",
            409: "Stock already exists for ingredient"
        }
    )
    def create(self, request):
        serializer = StockInsertSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        stock_response = self.init_stock_use_case.execute(**serializer.validated_data)
        
        return DjangoResponseWrapper.created(
            data=StockMappers.domain_to_dto(stock_response), 
            entity=f'Stock'
        )


    def update(self, request):
        serializer = StockInsertSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        stock_response = self.init_stock_use_case.execute(**serializer.validated_data)
        
        return DjangoResponseWrapper.updated(
            data=StockMappers.dto_to_dict(stock_response), 
            message=f'Stock'
            )

    @swagger_auto_schema(
        operation_description="Delete stock by ID",
        responses={
            200: "Stock successfully deleted",
            404: "Stock not found"
        }
    )
    def destroy(self, request, pk):
        self.delete_stock_use_case.execute(pk)
        return DjangoResponseWrapper.deleted('Stock')