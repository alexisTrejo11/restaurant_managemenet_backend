from rest_framework.viewsets import ViewSet
from core.response.django_response import DjangoResponseWrapper
from ...application.mapper.stock_mappers import StockTransactionMappers
from restaurant.serializers import StockInsertSerializer, StockSerializer, StockTransactionInsertSerializer
from core.injector.app_module import AppModule
from injector import Injector
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from ...application.use_case.stock_query_use_case import (
    GetStockHistoryUseCase,
    ListStocksUseCase,
    GetStockByIdUseCase,
    GenerateStockReportUseCase,
    GetStockByIngredientUseCase
) 

container = Injector([AppModule()])

class StockViews(ViewSet):
    def __init__(self, **kwargs):
        self.list_stock_use_case = container.get(ListStocksUseCase)
        self.get_stock_by_id_use_case = container.get(GetStockByIdUseCase)
        self.get_stock_by_ingredient_use_case = container.get(GetStockByIngredientUseCase)
        self.get_stock_history_use_case = container.get(GetStockHistoryUseCase)
        self.generate_stock_report_use_case = container.get(GenerateStockReportUseCase)
        super().__init__(**kwargs)

    permission_classes = [IsAuthenticated()]

    @swagger_auto_schema(
        operation_description="Get all stocks sorted by last transaction",
        responses={
            200: StockSerializer(many=True),
        }
    )
    def list(self, request):
        stock_list = self.list_stock_use_case.execute()
        
        stock_list_serialized = StockSerializer(stock_list, many=True).data

        return DjangoResponseWrapper.found(
            data=stock_list_serialized, 
            entity='Stock List'
            )


    @swagger_auto_schema(
        operation_description="Get stock by ID",
        responses={
            200: StockSerializer,
            404: "Stock not found"
        }
    )
    def retrieve(self, request, stock_id):
        stock = self.get_stock_by_id_use_case.execute(stock_id, include_transactions=True)

        stock_serialized = StockSerializer(stock).data
        
        return DjangoResponseWrapper.found(stock_serialized, 'Stock', 'stock_id', stock_id)


    @swagger_auto_schema(
        operation_description="Get stock by ingredient ID",
        responses={
            200: StockSerializer,
            404: "Ingredient not found or Stock not initialized"
        }
    )
    def retrieve_by_ingredient(self, request, ingredient_id):
        stock = self.get_stock_by_ingredient_use_case.execute(ingredient_id)
        if stock is None:
            return DjangoResponseWrapper.success( 
                message=f'Stock with ingredient Id [{ingredient_id}] has not been init'
            )

        stock_serialized = StockSerializer(stock).data
        return DjangoResponseWrapper.found(
            data=stock_serialized, 
            entity='Stock', 
            param='ingredient_id', 
            value=ingredient_id
        )

    def report(self, request):
        stock_report = self.generate_stock_report_use_case.execute()
       
        return DjangoResponseWrapper.success(
            data=stock_report, 
            message="Stock Report Succesfully Retrieved"
        )


    def history(self, request, stock_id):
        stock_history = self.get_stock_history_use_case.execute(stock_id)
       
        return DjangoResponseWrapper.success(
            data=stock_history, 
            message="Stock History Succesfully Retrieved"
        )