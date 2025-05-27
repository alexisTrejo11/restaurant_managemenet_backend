from rest_framework.viewsets import ViewSet
from shared.response.django_response import DjangoResponseWrapper as ResponseWrapper
from ..serializers.order_serializer import *
from payments.serializers import PaymentSerializer
from shared.injector.app_module import AppModule
from injector import Injector
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from shared.utils.permission import RoleBasedPermission
from rest_framework.permissions import IsAuthenticated
from ....application.use_case.order_command_use_case import (
    CreateOrderUseCase,
    UpdateOrderUseCase,
    DeleteOrderUseCase,
)
from ....application.use_case.order_query_use_case import (
    GetAllOrdersUseCase,
    GetOrderByIdUseCase,
    SearchOrdersUseCase
)
from rest_framework.decorators import action


class OrderViews(ViewSet):
    def __init__(self, **kwargs):
        self.search_orders_use_case = SearchOrdersUseCase()
        self.get_order_by_id_use_case = GetOrderByIdUseCase()
        self.get_all_orders_use_case = GetAllOrdersUseCase()
        self.create_order_use_case = CreateOrderUseCase()
        self.update_order_use_case = UpdateOrderUseCase()
        self.delete_order_use_case = DeleteOrderUseCase()
        super().__init__(**kwargs)

    def get_permissions(self):
        if self.action in ['delete_order', 'search_orders'] :
             return [RoleBasedPermission(['admin'])]
        else:
            return [IsAuthenticated()]

    @swagger_auto_schema(
        operation_description="Get order by ID",
        responses={
            200: OrderSerializer,
            404: "Order not found"
        }
    )
    def get_order_by_id(self, request, id):
        order_dto = self.get_order_by_id_use_case.execute(id, raise_exception=True)
        return ResponseWrapper.found(
            data=order_dto.to_dict(), 
            entity='Order',
            param='ID',
            value=id,
        )


class OrderViews(ViewSet):
    def __init__(self, **kwargs):
        self.search_orders_use_case = SearchOrdersUseCase()
        super().__init__(**kwargs)

    @swagger_auto_schema(
        operation_description="Search orders with dynamic filters",
        manual_parameters=[
            openapi.Parameter('status', openapi.IN_QUERY, description="Filter by order status", type=openapi.TYPE_STRING),
            openapi.Parameter('table_number', openapi.IN_QUERY, description="Filter by table number", type=openapi.TYPE_INTEGER),
            openapi.Parameter('created_at__gte', openapi.IN_QUERY, description="Filter by orders created after this date", type=openapi.TYPE_STRING),
            openapi.Parameter('created_at__lte', openapi.IN_QUERY, description="Filter by orders created before this date", type=openapi.TYPE_STRING),
            openapi.Parameter('end_at__isnull', openapi.IN_QUERY, description="Filter by orders with or without an end date", type=openapi.TYPE_BOOLEAN),
        ],
        responses={
            200: "Filtered orders",
            400: "Invalid filter parameters"
        }
    )
    @action(detail=False, methods=['GET'])
    def search_orders(self, request):
        """
        Search orders with dynamic filters based on query parameters.
        """
        search_filters = {
            'status': request.query_params.get('status'),
            'table__number': request.query_params.get('table_number'),
            'created_at__gte': request.query_params.get('created_at__gte'),
            'created_at__lte': request.query_params.get('created_at__lte'),
            'end_at__isnull': request.query_params.get('end_at__isnull'),
        }

        try:
            order_dto_list = self.search_orders_use_case.execute(search_filters)
        except ValueError as e:
            return ResponseWrapper.bad_request(str(e))

        order_dict_list = [dto.to_dict() for dto in order_dto_list]

        return ResponseWrapper.found(
            data=order_dict_list,
            entity='Filtered Orders'
        )

    @swagger_auto_schema(
        operation_description="Start a new order",
        responses={
            201: OrderSerializer,
            404: "Table not found",
            409: "Table not available"
        }
    )
    def start_order(self, request, table_number):
        order_service = self.get_order_service()
        table_service = self.get_table_service()

        table = table_service.get_table_by_number(table_number)
        if table is None:
            return ResponseWrapper.not_found(f'Table with {table_number} not found')
        elif not table.is_available:
            return ResponseWrapper.conflict(f'Table with number {table_number} is not available')

        order = order_service.init_order(table)        
        order_data = OrderSerializer(order).data

        return ResponseWrapper.created(order_data, 'Order Successfully Initialized')


    @swagger_auto_schema(
        operation_description="Add items to an existing order",
        request_body=OrderItemsInsertSerilizer,
        responses={
            200: OrderSerializer,
            400: "Bad request (Invalid data)"
        }
    )
    def add_items_to_order(self, request):
        order_service = self.get_order_service()

        serializer = OrderItemsInsertSerilizer(data=request.data)
        if not serializer.is_valid():
            return ResponseWrapper.bad_request(serializer.errors)
        
        order_id = serializer.data.get('order_id')

        order = order_service.get_order_by_id(order_id)
        if order is None:
            return ResponseWrapper.not_found('Order', 'ID', order_id)
        
        item_data = serializer.data.get('order_items')
        order_items = order_service.proccess_items(item_data)
        
        order_updated = order_service.add_items_to_order(order, order_items)

        order_data = OrderSerializer(order_updated).data
        return ResponseWrapper.ok(order_data, 'Order Successfully Updated')


    @swagger_auto_schema(
        operation_description="Delete items from an existing order",
        request_body=OrderItemsDeleteSerilizer,
        responses={
            200: OrderSerializer,
            400: "Bad request (Invalid data)"
        }
    )
    def delete_items_to_order(self, request):
        order_service = self.get_order_service()

        serializer = OrderItemsDeleteSerilizer(data=request.data)
        if not serializer.is_valid():
            return ResponseWrapper.bad_request(serializer.errors)
        
        order_id = serializer.data.get('order_id')
        order = order_service.get_order_by_id(order_id)
        if order is None:
            return ResponseWrapper.not_found('Order', 'ID', order_id)

        items_ids = serializer.data.get('item_ids')
        order_updated = order_service.delete_items_to_order(order, items_ids)
        
        order_data = OrderSerializer(order_updated).data
        return ResponseWrapper.ok(order_data, 'Order Successfully Updated')
    
    
    @swagger_auto_schema(
        operation_description="End an order (Payment pending)",
        responses={
            200: PaymentSerializer,
            404: "Order not found"
        }
    )
    def end_order(self, request, id):
        order_service = self.get_order_service()
        payment_service = self.get_payment_service()

        order = order_service.get_order_by_id(id)
        if order is None:
            return ResponseWrapper.not_found('Order', 'ID', id)

        order_service.end_order(order)
        
        payment = payment_service.create_payment(order)

        payment_data = PaymentSerializer(payment).data
        return ResponseWrapper.ok(payment_data, 'Order Successfully Ended. Payment is pending to be paid')
    

    @swagger_auto_schema(
        operation_description="Cancel an order",
        responses={
            200: "Order successfully cancelled",
            404: "Order not found"
        }
    )
    def cancel_order(self, request, id):
        order_service = self.get_order_service()

        order = order_service.get_order_by_id(id)
        if order is None:
            return ResponseWrapper.not_found('Order', 'ID', id)

        order_service.cancel_order(order)

        return ResponseWrapper.ok('Order Successfully Cancelled')
    

    @swagger_auto_schema(
        operation_description="Delete an order",
        responses={
            200: "Order successfully deleted",
            404: "Order not found"
        }
    )
    def delete_order(self, request, id):
        order_service = self.get_order_service()

        is_deleted = order_service.delete_order_by_id(id)
        if not is_deleted:
            return ResponseWrapper.not_found('Order', 'ID', id)

        return ResponseWrapper.ok('Order Successfully Deleted')
    
    
    @swagger_auto_schema(
        operation_description="Mark item as delivered",
        responses={
            200: "Item successfully set as delivered",
        }
    )
    def mark_item_as_delivered(self, request, order_id, item_id):
        order_service = self.get_order_service()

        order_service.set_item_as_delivered(order_id, item_id)

        return ResponseWrapper.ok('Item Successfully set as delivered')


    @swagger_auto_schema(
        operation_description="Get items not yet delivered",
        responses={
            200: OrderItemSerializer(many=True),
        }
    )
    def get_not_delivered_items(self, request):
        order_service = self.get_order_service()

        items = order_service.get_not_delivered_items()

        item_data = OrderItemSerializer(items, many=True).data
        return ResponseWrapper.ok(item_data, 'Order Items Successfully Fetched')
