from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from core.response.django_response import DjangoResponseWrapper as ResponseWrapper
from ..serializers.order_serializer import *
from restaurant_management.payments.service.payment_service import PaymentService
from core.injector.app_module import AppModule
from injector import Injector
from drf_yasg.utils import swagger_auto_schema
from core.utils.permission import RoleBasedPermission
from rest_framework.permissions import IsAuthenticated
from ....application.use_case.order_item_use_case import (
    AddOrderItemsUseCase,
    RemoveOrderItemUseCase,
    UpdateOrderItemUseCase
)

container = Injector([AppModule()])
class OrderItemApiView(APIView):
    def __init__(self, **kwargs):
        self.add_item_use_case =  container.get(AddOrderItemsUseCase)
        self.remove_item_use_case =  container.get(RemoveOrderItemUseCase)
        self.update_order_items_use_case =  container.get(UpdateOrderItemUseCase)
        super().__init__(**kwargs)

    @swagger_auto_schema(
        operation_description="Mark item as delivered",
        responses={
            200: "Item successfully set as delivered",
            404: "Order Item Not Found",
        }
    )
    def mark_item_as_delivered(self, request, item_id):
        delivered_statement = { "is_delivered" : True }
        
        self.update_order_items_use_case.execute(item_id, delivered_statement)
        
        return ResponseWrapper.success(message='Item Successfully set as delivered')


    def mark_item_as_not_delivered(self, request, item_id):
        delivered_statement = { "is_delivered" : False }
        
        self.update_order_items_use_case.execute(item_id, delivered_statement)
        
        return ResponseWrapper.success(message='Item Successfully set as not delivered')

    @swagger_auto_schema(
        operation_description="Add items to an existing order",
        request_body=OrderItemsInsertSerilizer,
        responses={
            200: OrderSerializer,
            400: "Bad request (Invalid data)"
        }
    )
    def add_items_to_order(self, request):
        # Add Serializer Validation
        serializer = OrderItemsInsertSerilizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        order_id = serializer.data.get('order_id')

        self.add_item_use_case.execute(
            order_id=order_id, 
            items_validate_data=serializer.data.get('order_items')
        )

        return ResponseWrapper.success(message='Order Item Successfully Added.')


    @swagger_auto_schema(
        operation_description="Delete items from an existing order",
        request_body=OrderItemsDeleteSerilizer,
        responses={
            200: OrderSerializer,
            400: "Bad request (Invalid data)"
        }
    )
    def remove_items_to_order(self, request):
        # Add Serializer Validation
        serializer = OrderItemsDeleteSerilizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        order_id = serializer.data.get('order_id')

        self.remove_item_use_case.execute(
            order_id=order_id, 
            items_validate_data=serializer.data.get('item_ids')
        )

        return ResponseWrapper.success(message='Order Item Successfully Added.')