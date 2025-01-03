from rest_framework.viewsets import ViewSet
from restaurant.utils.response import ApiResponse
from restaurant.serializers import OrderSerializer, OrderItemSerializer ,OrderItemsInsertSerilizer, OrderItemsDeleteSerilizer, PaymentSerializer
from restaurant.services.order_service import OrderService
from restaurant.services.table_service import TableService
from restaurant.services.payment_service import PaymentService
from restaurant.injector.app_module import AppModule
from injector import Injector

container = Injector([AppModule()])

class OrderViews(ViewSet):
    def get_order_service(self):
        return container.get(OrderService)

    def get_table_service(self):
        return container.get(TableService)
    
    def get_payment_service(self):
        return container.get(PaymentService)
    
    
    def get_order_by_id(self, request, id):
        order_service = self.get_order_service()

        order = order_service.get_order_by_id(id)
        if order is None:
            return ApiResponse.not_found('Order', 'id', id)

        order_data = OrderSerializer(order).data
        return ApiResponse.found(order_data, 'Order', 'ID', id)


    def get_orders_by_status(self, request, status):
        order_service = self.get_order_service()

        orders = order_service.get_orders_by_status(status)
        
        order_data = OrderSerializer(orders, many=True).data
        return ApiResponse.ok(order_data, f'Order with status [{status}] not found')


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
    
    
    def end_order(self, request, id):
        order_service = self.get_order_service()
        payment_service = self.get_pa()

        order = order_service.get_order_by_id(id)
        if order is None:
            return ApiResponse.not_found('Order', 'ID', id)

        order_service.end_order(order)
        payment = payment_service.create_payment(order)

        payment_data = PaymentSerializer(payment).data
        return ApiResponse.ok(payment_data, 'Order Successfully Ended. Payment is pending to be paid')
    

    def cancel_order(self, request, id):
        order_service = self.get_order_service()

        order = order_service.get_order_by_id(id)
        if order is None:
            return ApiResponse.not_found('Order', 'ID', id)

        order_service.cancel_order(order)

        return ApiResponse.ok('Order Successfully Cancelled')
    

    def delete_order(self, request, id):
        order_service = self.get_order_service()

        is_deleted = order_service.delete_order_by_id(id)
        if not is_deleted:
            return ApiResponse.not_found('Order', 'ID', id)

        return ApiResponse.ok('Order Successfully Deleted')
    
    
    def mark_item_as_delivered(self, request, order_id, item_id):
        order_service = self.get_order_service()

        order_service.set_item_as_delivered(order_id, item_id)

        return ApiResponse.ok('Item Successfully set as delivered')


    def get_not_delivered_items(self, request):
        order_service = self.get_order_service()

        items = order_service.get_not_delivered_items()

        item_data = OrderItemSerializer(items, many=True).data
        return ApiResponse.ok(item_data, 'Order Items Succesfully Fetched')
    
