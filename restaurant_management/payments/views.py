from rest_framework.viewsets import ViewSet
from restaurant_management.payments.service.payment_service import PaymentService
from common.utils.response import ApiResponse
from restaurant.serializers import PaymentSerializer
from datetime import datetime
from common.injector.app_module import AppModule
from injector import Injector
from drf_yasg.utils import swagger_auto_schema
from common.utils.permission import RoleBasedPermission

container = Injector([AppModule()])

class PaymentViews(ViewSet):
    # Role Permissions
    def get_permissions(self):
        return [RoleBasedPermission(['admin'])]

    # Payment Service injection
    def get_payment_service(self):
        return container.get(PaymentService)

    @swagger_auto_schema(
        operation_description="Get payment by ID",
        responses={
            200: PaymentSerializer,
            404: "Payment not found"
        }
    )
    def get_payment_by_id(self, request, id):
        payment_service = self.get_payment_service()

        payment = payment_service.get_payment_by_id(id)
        if not payment:
            return ApiResponse.not_found('Payment', 'ID', id)
        
        payment_data = PaymentSerializer(payment).data 
        return ApiResponse.found(payment_data, 'Payment', 'ID', id)


    @swagger_auto_schema(
        operation_description="Get payments by status",
        responses={
            200: PaymentSerializer(many=True),
            400: "Invalid payment status"
        }
    )
    def get_payments_by_status(self, request, status):
        payment_service = self.get_payment_service()

        payment_valid = payment_service.valdiate_payment_status(status)
        if not payment_valid:
            return ApiResponse.bad_request('Invalid payment status')

        payments = payment_service.get_payments_by_status(status)
        
        payment_data = PaymentSerializer(payments, many=True).data 
        return ApiResponse.ok(payment_data, f'Payments with status [{status}] successfully fetched')


    @swagger_auto_schema(
        operation_description="Get payments by date range",
        responses={
            200: PaymentSerializer(many=True),
            400: "Invalid date format"
        }
    )
    def get_payments_by_data_range(self, request, start_date, end_date):
        payment_service = self.get_payment_service()
        
        if isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date)
        if isinstance(end_date, str):
            end_date = datetime.fromisoformat(end_date)
        
        payments = payment_service.get_complete_payments_by_date_range(start_date, end_date)
    
        payment_data = PaymentSerializer(payments, many=True).data 
        return ApiResponse.ok(payment_data, f'Payments between {start_date} and {end_date} successfully fetched')


    @swagger_auto_schema(
        operation_description="Get today's payments",
        responses={
            200: PaymentSerializer(many=True),
        }
    )
    def get_today_payments(self, request):
        payment_service = self.get_payment_service()

        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)

        payments = payment_service.get_complete_payments_by_date_range(start_date, end_date)
        
        payment_data = PaymentSerializer(payments, many=True).data 
        return ApiResponse.ok(payment_data, 'Today payments successfully fetched')


    @swagger_auto_schema(
        operation_description="Complete a payment",
        responses={
            200: PaymentSerializer,
            404: "Payment not found",
            409: "Conflict (payment validation failure)"
        }
    )
    def complete_payment(self, request, id, payment_method):
        payment_service = self.get_payment_service()

        payment = payment_service.get_payment_by_id(id)
        if not payment:
            return ApiResponse.not_found('Payment', 'ID', id)
        
        validate_result = payment_service.validate_payment_complete(payment)
        if validate_result.is_failure():
            return ApiResponse.conflict(validate_result.get_error_msg())

        payment_complete = payment_service.complete_payment(payment, payment_method)
        if payment_complete.is_failure():
            return ApiResponse.conflict(validate_result.get_error_msg())

        payment_data = PaymentSerializer(payment_complete.get_data()).data 
        return ApiResponse.ok(payment_data, 'Payment successfully completed') 


    @swagger_auto_schema(
        operation_description="Cancel a payment",
        responses={
            200: "Payment successfully cancelled",
            404: "Payment not found",
            409: "Conflict (payment validation failure)"
        }
    )
    def cancel_payment(self, request, id):
        payment_service = self.get_payment_service()

        payment = payment_service.get_payment_by_id(id)
        if not payment:
            return ApiResponse.not_found('Payment', 'ID', id)
        
        validate_result = payment_service.validate_payment_cancel(payment)
        if validate_result.is_failure():
            return ApiResponse.conflict(validate_result.get_error_msg())

        payment_service.update_payment_status(payment, 'CANCELLED')

        return ApiResponse.ok(None, 'Payment successfully cancelled')
