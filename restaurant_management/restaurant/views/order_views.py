
from rest_framework.viewsets import ViewSet
from restaurant.utils.response import ApiResponse
from restaurant.serializers import OrderSerializer


class OrderView:
    def get_order_by_id(request, order_id):
        order_result = OrderService.get_order_by_id(order_id)

        if order_result.is_failure():
            return ApiResponse.not_found(order_result.get_error_msg())
        
        order_data = OrderSerializer(order_result.get_data()).data
        return ApiResponse.ok(order_data, f'Order with ID {order_id} not found')

"""
@api_view(['GET'])
def get_orders_by_status(request, order_status):
     order_result = OrderService.get_orders_by_status(order_status)

     if order_result.is_failure():
          return ApiResponse.bad_request(order_result.get_error_msg())
     
     order_data = OrderSerializer(order_result.get_data(), many=True).data
     return ApiResponse.ok(order_data, f'Orders with status:{order_status} succesfully fetched')


@api_view(['POST'])
def init_order(request):
     serializer = OrderInsertSerializer(data=request.data)
     if not serializer.is_valid():
        return ApiResponse.bad_request(serializer.errors)
     
     table_number = request.data.get('table_number')
     table = TableService.get_table_by_number(table_number)
     if table is None:
          return ApiResponse.not_found(f'Table with {table_number} not found')
     elif not table.is_available:
          return ApiResponse.conflict(f'Table with number {table_number} is not available')

     order_item_dtos = OrderMappers.map_request_to_order_item_dtos(request.data)

     order = OrderService.init_order(table=table, order_items_dtos=order_item_dtos)

     order_data = OrderSerializer(order).data
     return ApiResponse.ok(order_data, 'Order Successfully Initialized')


@api_view(['PUT'])
def add_items_to_order(request, order_id):
     serializer = AddItemsSerilizer(data=request.data)
     if not serializer.is_valid():
        return ApiResponse.bad_request(serializer.errors)
     
     order_item_dtos = OrderMappers.map_request_to_order_item_dtos(request.data)

     order_result = OrderService.get_order_by_id(order_id)
     if order_result.is_failure():
          return ApiResponse.not_found(order_result.get_error_msg())
     
     order_updated = OrderService.add_items_to_order(order_result.get_data(), order_item_dtos)
     order_data = OrderSerializer(order_updated).data

     return ApiResponse.ok(order_data, f'Items Successfully Added. Update:{len(order_item_dtos)} items added')


@api_view(['PUT'])
def finish_order(request, order_id):
     order_result = OrderService.get_order_by_id(order_id)
     if order_result.is_failure():
          return ApiResponse.not_found(order_result.get_error_msg())

     OrderService.update_order_status(order_result.get_data(), 'completed')

     table = order_result.get_data().table
     OrderService.set_table_as_available(table)

     order = order_result.get_data()
     
     valdiation_result = PaymentService.validate_payment_creation(order)
     if valdiation_result.is_failure():
          return ApiResponse.conflict(valdiation_result.get_error_msg())

     payment = PaymentService.init_payment(order)
     
     payment_data = PaymentSerializer(payment).data
     return ApiResponse.ok(payment_data, 'Order succesfully finished. Payment is waiting to be paid!.')


@api_view(['PUT'])
def cancel_order(request, order_id):
     order_result = OrderService.get_order_by_id(order_id)
     if order_result.is_failure():
          return ApiResponse.not_found(order_result.get_error_msg())
     
     verify_result = OrderService.verify_order_cancel(order_result.get_data())
     if verify_result.is_failure():
          return ApiResponse.bad_request(verify_result.get_error_msg())

     OrderService.update_order_status(order, 'cancelled')

     return ApiResponse.ok('Order succesfully cancelled')
"""