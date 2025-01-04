from rest_framework.viewsets import ViewSet
from restaurant.services.stock_service import StockService
from restaurant.services.ingredient_service import IngredientService
from restaurant.utils.response import ApiResponse
from restaurant.mappers.stock_mappers import StockTransactionMappers
from restaurant.serializers import StockInsertSerializer, StockSerializer, StockTransactionInsertSerializer
from restaurant.injector.app_module import AppModule
from injector import Injector
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status

container = Injector([AppModule()])

class StockViews(ViewSet):
    def get_ingredient_service(self):
        return container.get(IngredientService)

    def get_stock_service(self):
        return container.get(StockService)

    @swagger_auto_schema(
        operation_description="Get all stocks sorted by last transaction",
        responses={
            200: StockSerializer(many=True),
        }
    )
    def get_all_stocks_sort_by_last_transaction(self, request):
        stock_service = self.get_stock_service()

        stock_list = stock_service.get_all_stocks_sort_by_last_transaction()
        stock_list_serialized = StockSerializer(stock_list, many=True).data
        return ApiResponse.ok(stock_list_serialized, 'Stock List Successfully Fetched')


    @swagger_auto_schema(
        operation_description="Get stock by ID",
        responses={
            200: StockSerializer,
            404: "Stock not found"
        }
    )
    def get_stock_by_id(self, request, stock_id):
        stock_service = self.get_stock_service()

        stock = stock_service.get_stock_by_id(stock_id)
        if stock is None:
            return ApiResponse.not_found('Stock', 'ID', stock_id)

        stock_serialized = StockSerializer(stock).data
        return ApiResponse.found(stock_serialized, 'Stock', 'stock_id', stock_id)


    @swagger_auto_schema(
        operation_description="Get stock by ingredient ID",
        responses={
            200: StockSerializer,
            404: "Ingredient not found or Stock not initialized"
        }
    )
    def get_stock_by_ingredient_id(self, request, ingredient_id):
        stock_service = self.get_stock_service()
        ingredient_service = self.get_ingredient_service()

        ingredient = ingredient_service.get_ingredient_by_id(ingredient_id)
        if ingredient is None:
            return ApiResponse.not_found('Ingredient', 'ID', ingredient_id )

        stock = stock_service.get_stock_by_ingredient(ingredient)
        if stock is None:
            return ApiResponse.ok(None, f'Stock with ingredient Id [{ingredient_id}] has not been init')

        stock_serialized = StockSerializer(stock).data
        return ApiResponse.found(stock_serialized, 'Stock', 'ingredient_id', ingredient_id)


    @swagger_auto_schema(
        operation_description="Initialize stock for an ingredient",
        request_body=StockInsertSerializer,
        responses={
            200: StockSerializer,
            400: "Invalid data or Ingredient not found",
            409: "Stock already exists for ingredient"
        }
    )
    def init_stock(self, request):
        stock_service = self.get_stock_service()
        ingredient_service = self.get_ingredient_service()

        serializer = StockInsertSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse.bad_request(serializer.errors)
        
        ingredient_id = serializer.validated_data.get('ingredient_id')
        ingredient = ingredient_service.get_ingredient_by_id(ingredient_id)
        if ingredient is None:
            return ApiResponse.not_found('Ingredient', 'ID', ingredient_id)

        is_stock_unique = stock_service.validate_unique_stock_per_product(ingredient)
        if not is_stock_unique:
            return ApiResponse.ok(None, f'Ingredient Id [{ingredient_id}] already has stock')

        stock = stock_service.init_stock(ingredient, serializer.validated_data)
        stock_serialized = StockSerializer(stock).data
        
        return ApiResponse.ok(stock_serialized, f'Stock with ingredient Id {ingredient_id} successfully init')


    @swagger_auto_schema(
        operation_description="Add a transaction to stock",
        request_body=StockTransactionInsertSerializer,
        responses={
            200: StockSerializer,
            400: "Invalid transaction data or Stock not found"
        }
    )
    def add_transaction(self, request):
        stock_service = self.get_stock_service()

        serializer = StockTransactionInsertSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse.bad_request(serializer.errors)

        stock_id = serializer.validated_data.get('stock_id')
        stock = stock_service.get_stock_by_id(stock_id)
        if stock is None:
            return ApiResponse.not_found('Stock', 'ID', stock_id)

        trasaction = StockTransactionMappers.serializerToDomain(serializer.validated_data)
        trasaction.stock = stock

        validation_result = stock_service.validate_transaction(stock, trasaction)
        if (validation_result.is_failure()):
            return ApiResponse.bad_request(validation_result.get_error_msg())

        stock = stock_service.add_transaction(stock, trasaction)
        stock_serialized = StockSerializer(stock).data
        
        return ApiResponse.ok(stock_serialized, 'Transaction successfully added')


    @swagger_auto_schema(
        operation_description="Delete stock by ID",
        responses={
            200: "Stock successfully deleted",
            404: "Stock not found"
        }
    )
    def delete_stock_by_id(self, request, pk):
        stock_service = self.get_stock_service()

        is_deleted = stock_service.delete_stock_by_id(pk)
        if not is_deleted:
            return ApiResponse.not_found('Stock', 'ID', pk)

        return ApiResponse.deleted('Stock')
