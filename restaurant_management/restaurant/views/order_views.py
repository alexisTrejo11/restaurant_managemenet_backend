from rest_framework.viewsets import ViewSet
from restaurant.utils.response import ApiResponse
from restaurant.serializers import OrderSerializer, OrderItemSerializer, OrderItemsInsertSerilizer, OrderItemsDeleteSerilizer, PaymentSerializer
from restaurant.services.order_service import OrderService
from restaurant.services.table_service import TableService
from restaurant.services.payment_service import PaymentService
from restaurant.injector.app_module import AppModule
from injector import Injector
from drf_yasg.utils import swagger_auto_schema

container = Injector([AppModule()])

class OrderViews(ViewSet):
    def get_order_service(self):
        return container.get(OrderService)

    def get_table_service(self):
        return container.get(TableService)
    
    def get_payment_service(self):
        return container.get(PaymentService)

    @swagger_auto_schema(
        operation_description="Get order by ID",
        responses={
            200: OrderSerializer,
            404: "Order not found"
        }
    )
    def get_order_by_id(self, request, id):
        order_service = self.get_order_service()

        order = order_service.get_order_by_id(id)
        if order is None:
            return ApiResponse.not_found('Order', 'ID', id)

        order_data = OrderSerializer(order).data
        return ApiResponse.found(order_data, 'Order', 'ID', id)


    @swagger_auto_schema(
        operation_description="Get orders by status",
        responses={
            200: OrderSerializer(many=True),
            404: "Orders with specified status not found"
        }
    )
    def get_orders_by_status(self, request, status):
        order_service = self.get_order_service()

        orders = order_service.get_orders_by_status(status)
        
        order_data = OrderSerializer(orders, many=True).data
        return ApiResponse.ok(order_data, f'Order with status [{status}] not found')


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
            return ApiResponse.not_found(f'Table with {table_number} not found')
        elif not table.is_available:
            return ApiResponse.conflict(f'Table with number {table_number} is not available')

        order = order_service.init_order(table)        
        order_data = OrderSerializer(order).data

        return ApiResponse.created(order_data, 'Order Successfully Initialized')


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
            return ApiResponse.bad_request(serializer.errors)
        
        order_id = serializer.data.get('order_id')

        order = order_service.get_order_by_id(order_id)
        if order is None:
            return ApiResponse.not_found('Order', 'ID', order_id)
        
        item_data = serializer.data.get('order_items')
        order_items = order_service.proccess_items(item_data)
        
        order_updated = order_service.add_items_to_order(order, order_items)

        order_data = OrderSerializer(order_updated).data
        return ApiResponse.ok(order_data, 'Order Successfully Updated')


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
            return ApiResponse.bad_request(serializer.errors)
        
        order_id = serializer.data.get('order_id')
        order = order_service.get_order_by_id(order_id)
        if order is None:
            return ApiResponse.not_found('Order', 'ID', order_id)

        items_ids = serializer.data.get('item_ids')
        order_updated = order_service.delete_items_to_order(order, items_ids)
        
        order_data = OrderSerializer(order_updated).data
        return ApiResponse.ok(order_data, 'Order Successfully Updated')
    
    
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
            return ApiResponse.not_found('Order', 'ID', id)

        order_service.end_order(order)
        payment = payment_service.create_payment(order)

        payment_data = PaymentSerializer(payment).data
        return ApiResponse.ok(payment_data, 'Order Successfully Ended. Payment is pending to be paid')
    

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
            return ApiResponse.not_found('Order', 'ID', id)

        order_service.cancel_order(order)

        return ApiResponse.ok('Order Successfully Cancelled')
    

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
            return ApiResponse.not_found('Order', 'ID', id)

        return ApiResponse.ok('Order Successfully Deleted')
    
    
    @swagger_auto_schema(
        operation_description="Mark item as delivered",
        responses={
            200: "Item successfully set as delivered",
        }
    )
    def mark_item_as_delivered(self, request, order_id, item_id):
        order_service = self.get_order_service()

        order_service.set_item_as_delivered(order_id, item_id)

        return ApiResponse.ok('Item Successfully set as delivered')


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
        return ApiResponse.ok(item_data, 'Order Items Successfully Fetched')
