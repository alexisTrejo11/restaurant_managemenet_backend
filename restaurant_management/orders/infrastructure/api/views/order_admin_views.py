from rest_framework.viewsets import ViewSet
from shared.response.django_response import DjangoResponseWrapper as ResponseWrapper
from ..serializers.order_serializer import OrderSerializer
from shared.injector.app_module import AppModule
from injector import Injector
from drf_yasg.utils import swagger_auto_schema
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
        operation_description="Get order by ID",
        responses={
            200: OrderSerializer,
            404: "Order not found"
        }
    )
    def retrieve(self, request, id):
        """
        Retrieve an order by its ID.
        """
        order_dto = self.get_order_by_id_use_case.execute(id, raise_exception=True)
        return ResponseWrapper.found(
            data=order_dto.to_dict(),
            entity='Order',
            param='ID',
            value=id,
        )

    @swagger_auto_schema(
        operation_description="Get all orders",
        responses={
            200: OrderSerializer(many=True),
            404: "No orders found"
        }
    )
    def list(self, request):
        """
        Retrieve all orders.
        """
        order_dto_list = self.get_all_orders_use_case.execute()
        order_dict_list = [dto.to_dict() for dto in order_dto_list]
        return ResponseWrapper.found(
            data=order_dict_list,
            entity='All Orders'
        )

    @swagger_auto_schema(
        operation_description="Create a new order",
        request_body=OrderSerializer,
        responses={
            201: OrderSerializer,
            400: "Bad request (Invalid data)"
        }
    )
    def create(self, request):
        """
        Create a new order.
        """
        serializer = OrderSerializer(data=request.data)
        if not serializer.is_valid():
            return ResponseWrapper.bad_request(serializer.errors)

        # Convert validated data to domain entity
        order_data = serializer.validated_data
       
        # Execute the use case
        created_order = self.create_order_use_case.execute(order_data)
        return ResponseWrapper.created(
            data=created_order.to_dict(),
            message="Order Successfully Created"
        )

    @swagger_auto_schema(
        operation_description="Update an existing order",
        request_body=OrderSerializer,
        responses={
            200: OrderSerializer,
            400: "Bad request (Invalid data)",
            404: "Order not found"
        }
    )
    def update(self, request, id):
        """
        Update an existing order.
        """
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # ???
        order = self.get_object()
        order_update_data = serializer.validated_data

        updated_order = self.update_order_use_case.execute(exisiting_order=order, **order_update_data)
        return ResponseWrapper.ok(
            data=updated_order.to_dict(),
            message="Order Successfully Updated"
        )

    @swagger_auto_schema(
        operation_description="Delete an order",
        responses={
            200: "Order successfully deleted",
            404: "Order not found"
        }
    )
    def destroy(self, request, id):
        """
        Delete an order.
        """
        self.delete_order_use_case.execute(id)
        return ResponseWrapper.ok(message="Order Successfully Deleted")