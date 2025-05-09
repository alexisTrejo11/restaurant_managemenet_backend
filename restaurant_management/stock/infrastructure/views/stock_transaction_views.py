from rest_framework.viewsets import ViewSet
from core.response.django_response import DjangoResponseWrapper
from ...application.mapper.stock_mappers import StockMappers
from ...serializers import StockInsertSerializer, StockSerializer, StockTransactionInsertSerializer
from core.injector.app_module import AppModule
from injector import Injector
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from ...application.use_case.stock_transaction_use_case import (
    RegisterStockMovementUseCase,
    AdjustStockMovementUseCase,
    DeleteStockMovementUseCase

) 
from injector import Injector


container = Injector([AppModule()])

class StockTransactionViews:
    def __init__(self, register_movement):
        self.register_movement =  container.get(RegisterStockMovementUseCase)
        self.update_movement =  container.get(AdjustStockMovementUseCase)
        self.delete_movement =  container.get(DeleteStockMovementUseCase)
        pass

    @swagger_auto_schema(
        operation_description="Record a transaction to stock",
        request_body=StockTransactionInsertSerializer,
        responses={
            200: StockSerializer,
            400: "Invalid transaction data or Stock not found"
        }
    )
    def create(self, request):
        serializer = StockTransactionInsertSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        transaction_details = self.stock_movement_use_case.execute()
        
        return DjangoResponseWrapper.created(
            data=StockMappers.dto_to_dict(transaction_details),
            entity='Stock Transaction'
        )
    
    def update(self, request):
        serializer = StockTransactionInsertSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        transaction_details = self.update_movement.execute(**serializer.validated_data)
        
        return DjangoResponseWrapper.created(
            data=StockMappers.dto_to_dict(transaction_details),
            entity='Stock Transaction'
        )


    def destroy(self, request, pk):
        self.delete_movement.execute(pk)
        
        return DjangoResponseWrapper.success(
            message='Stock Transaction Successfully Deleted'
        )
