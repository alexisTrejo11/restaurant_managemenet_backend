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
    UpdateOrderItemUseCase,
    SetItemDeliveredStausUseCase
)

container = Injector([AppModule()])

class OrderItemApiView(APIView):
    def __init__(self, **kwargs):
        self.update_order_items_use_case =  container.get(UpdateOrderItemUseCase)
        self.set_item_delivered_use_case =  container.get(SetItemDeliveredStausUseCase)
        super().__init__(**kwargs)

    @swagger_auto_schema(
        operation_description="Update delivery status of an order item",
        #request_body=SetDeliveredStatusSerializer, # Un serializador para { "is_delivered": true/false }
        responses={
            200: "Item delivery status updated successfully",
            400: "Bad request (Invalid data)",
            404: "Order Item Not Found",
        }
    )
    def patch(self, request, item_id):
        # serializer = SetDeliveredStatusSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # is_delivered = serializer.validated_data['is_delivered']
        self.set_item_delivered_use_case.execute(item_id, True)
        return ResponseWrapper.success(message='Item delivery status updated successfully')

    @swagger_auto_schema(
        operation_description="Update items to an existing order",
        request_body=OrderItemsInsertSerilizer,
        responses={
            200: OrderSerializer,
            400: "Bad request (Invalid data)"
        }
    )
    def put(self, request):
        serializer = OrderItemsInsertSerilizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_id = serializer.data.get('order_id')
        self.update_order_items_use_case.execute(
            order_id=order_id,
            items_validate_data=serializer.data.get('order_items')
        )
        return ResponseWrapper.success(message='Order Items successfully updated. Changes will be sent to Kitchen')
    
    def _parse_param_to_bool(self, parse_str) -> bool:
        if parse_str or parse_str == '':
            raise ValueError('is_delivered is obligatory')
        elif parse_str.lower().strip() == 'false':
            return False
        elif parse_str.lower().strip() == 'true':
            return True
        else:
            raise ValueError('Invalid Delivered Value: must be true or false')