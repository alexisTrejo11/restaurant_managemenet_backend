from rest_framework.viewsets import ViewSet
from core.response.django_response import DjangoResponseWrapper as ResponseWrapper
from ..serializers.order_serializer import OrderSerializer
from payments.serializers import PaymentSerializer
from core.injector.app_module import AppModule
from injector import Injector
from drf_yasg.utils import swagger_auto_schema
from core.utils.permission import RoleBasedPermission
from rest_framework.permissions import IsAuthenticated
from ....application.use_case.order_command_use_case import (
    CreateOrderUseCase,
    UpdateOrderUseCase,
    DeleteOrderUseCase,
)
from ....application.use_case.order_query_use_case import (
    GetAllOrdersUseCase,
    GetOrderByIdUseCase,
)


class OrderViews(ViewSet):
    def __init__(self, **kwargs):
        self.get_order_by_id_use_case = GetOrderByIdUseCase()
        self.get_all_orders_use_case = GetAllOrdersUseCase()
        self.create_order_use_case = CreateOrderUseCase()
        self.update_order_use_case = UpdateOrderUseCase()
        self.delete_order_use_case = DeleteOrderUseCase()
        super().__init__(**kwargs)

    def get_permissions(self):
        if self.action == 'delete_order':
             return [RoleBasedPermission(['admin'])]
        else:
            return [IsAuthenticated()]


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
    def soft_delete_order(self, request, id):
        order_service = self.get_order_service()

        is_deleted = order_service.delete_order_by_id(id)
        if not is_deleted:
            return ResponseWrapper.not_found('Order', 'ID', id)

        return ResponseWrapper.ok('Order Successfully Deleted')