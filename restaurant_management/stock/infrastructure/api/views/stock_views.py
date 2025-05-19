# Django
from rest_framework.viewsets import ViewSet
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from ..serializers.serializers import StockInsertSerializer, StockSerializer
from core.response.django_response import DjangoResponseWrapper
from rest_framework.decorators import action
# Use Case
from stock.application.use_case.stock_query_use_case import (
    GetStockHistoryUseCase,
    ListStocksUseCase,
    GetStockByIdUseCase,
    GenerateStockReportUseCase,
    GetStockByIngredientUseCase
)
from stock.application.use_case.stock_command_use_case import (
    CreateStockUseCase,
    UpdateStockUseCase,
    DeleteStockUseCase
)
# Inject
from core.injector.stock_container import StockContainer
from dependency_injector.wiring import Provide

class StockViews(ViewSet):
    permission_classes = [IsAuthenticated]

    def __init__(
        self,
        list_stock_use_case: ListStocksUseCase = Provide[StockContainer.clear_stock_use_case],
        get_stock_by_id_use_case: GetStockByIdUseCase = Provide[StockContainer.get_stock_by_id_use_case],
        get_stock_by_ingredient_use_case: GetStockByIngredientUseCase = Provide[StockContainer.get_stock_by_ingredient_use_case],
        get_stock_history_use_case: GetStockHistoryUseCase = Provide[StockContainer.get_stock_history_use_case],
        generate_stock_report_use_case: GenerateStockReportUseCase = Provide[StockContainer.generate_stock_use_case],
        create_stock_use_case: CreateStockUseCase = Provide[StockContainer.create_stock_use_case],
        update_stock_use_case: UpdateStockUseCase = Provide[StockContainer.update_stock_use_case],
        delete_stock_use_case: DeleteStockUseCase = Provide[StockContainer.delete_stock_use_case],
        **kwargs
    ):
        super().__init__(**kwargs)

        self.list_stock_use_case = list_stock_use_case
        self.get_stock_by_id_use_case = get_stock_by_id_use_case
        self.get_stock_by_ingredient_use_case = get_stock_by_ingredient_use_case
        self.get_stock_history_use_case = get_stock_history_use_case
        self.generate_stock_report_use_case = generate_stock_report_use_case
        self.create_stock_use_case = create_stock_use_case
        self.update_stock_use_case = update_stock_use_case
        self.delete_stock_use_case = delete_stock_use_case

    @swagger_auto_schema(
        operation_description="Get all stocks sorted by last transaction",
        responses={200: StockSerializer(many=True)}
    )
    def list(self, request):
        stock_list = self.list_stock_use_case.execute()
        serialized = StockSerializer(stock_list, many=True).data
        return DjangoResponseWrapper.found(data=serialized, entity='Stock')

    @swagger_auto_schema(
        operation_description="Get stock by ID",
        responses={200: StockSerializer, 404: "Not Found"}
    )
    def retrieve(self, request, pk=None):
        stock = self.get_stock_by_id_use_case.execute(pk)
        if not stock:
            return DjangoResponseWrapper.not_found(entity='Stock', value=pk)
        return DjangoResponseWrapper.found(StockSerializer(stock).data, 'Stock')

    @swagger_auto_schema(
        operation_description="Create new stock",
        request_body=StockInsertSerializer,
        responses={201: StockSerializer, 400: "Invalid data"}
    )
    def create(self, request):
        serializer = StockInsertSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        stock = self.create_stock_use_case.execute(**serializer.validated_data)
        return DjangoResponseWrapper.created(data=StockSerializer(stock).data, entity='Stock')

    @swagger_auto_schema(
        operation_description="Update existing stock",
        request_body=StockInsertSerializer,
        responses={200: StockSerializer, 400: "Invalid data", 404: "Not Found"}
    )
    def update(self, request, pk=None):
        serializer = StockInsertSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        stock = self.update_stock_use_case.execute(pk, **serializer.validated_data)
        return DjangoResponseWrapper.updated(data=StockSerializer(stock).data, message='Stock updated')

    @swagger_auto_schema(
        operation_description="Delete stock by ID",
        responses={200: "Deleted", 404: "Not Found"}
    )
    def destroy(self, request, pk=None):
        self.delete_stock_use_case.execute(pk)
        return DjangoResponseWrapper.deleted('Stock')

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        history = self.get_stock_history_use_case.execute(stock_id=pk)
        return DjangoResponseWrapper.success(data=history, message='Stock History')

    @action(detail=False, methods=['get'])
    def report(self, request):
        report = self.generate_stock_report_use_case.execute()
        return DjangoResponseWrapper.success(data=report, message='Stock Report')

    @action(detail=False, methods=['get'], url_path='by-ingredient/(?P<ingredient_id>[^/.]+)')
    def retrieve_by_ingredient(self, request, ingredient_id=None):
        stock = self.get_stock_by_ingredient_use_case.execute(ingredient_id)
        if not stock:
            return DjangoResponseWrapper.success(message=f"No stock for ingredient {ingredient_id}")
        return DjangoResponseWrapper.found(data=StockSerializer(stock).data, entity='Stock')