"""
from django.shortcuts import render
from rest_framework.decorators import api_view
from restaurant.services.payment_service import PaymentService
from restaurant.utils.response import ApiResponse
from restaurant.utils.result import Result
from restaurant.serializers import PaymentSerializer, CompletePaymentSerializer
from datetime import datetime

@api_view(['GET'])
def get_payment_by_id(request, payment_id):
     payment_result = PaymentService.get_payment_by_id(payment_id)
     
     if payment_result.is_failure():
          return ApiResponse.not_found(payment_result.get_error_msg())
     
     payment_data = PaymentSerializer(payment_result.get_data()).data 
     return ApiResponse.ok(payment_data, f'Paymment with ID {payment_id} succesfully fetched')


@api_view(['GET'])
def get_payments_by_status(request, payment_status):
     payment_valid = PaymentService.valdiate_payment_status(payment_status)
     if not payment_valid:
          return ApiResponse.bad_request('Invalid payment status')

     payments = PaymentService.get_payments_by_status(payment_status)
     
     payment_data = PaymentSerializer(payments, many=True).data 
     return ApiResponse.ok(payment_data, 'Payments with status {payment_status} succesfully fetched')


@api_view(['GET'])
def get_payments_by_data_range(request, start_date, end_date):
     if isinstance(start_date, str):
          start_date = datetime.fromisoformat(start_date)
     if isinstance(end_date, str):
          end_date = datetime.fromisoformat(end_date)
    
     payment_result = PaymentService.get_complete_payments_by_date_range(start_date, end_date)
     
     if payment_result.is_failure():
          return ApiResponse.bad_request(payment_result.get_error_msg())
     
     payment_data = PaymentSerializer(payment_result.get_data(), many=True).data 
     return ApiResponse.ok(payment_data, f'Paymments with data between {start_date} and {end_date} succesfully fetched')


@api_view(['GET'])
def get_today_payments(request):
     start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
     end_date = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)

     payment_result = PaymentService.get_complete_payments_by_date_range(start_date, end_date)
     if payment_result.is_failure():
          return ApiResponse.bad_request(payment_result.get_error_msg())
     
     payment_data = PaymentSerializer(payment_result.get_data(), many=True).data 
     return ApiResponse.ok(payment_data, 'Today Payments succesfully fetched')


@api_view(['PUT'])
def complete_payment(request, payment_id):
     serializer = CompletePaymentSerializer(data=request.data)
     if not serializer.is_valid():
          return ApiResponse.bad_request(serializer.errors)

     payment_result = PaymentService.get_payment_by_id(payment_id)
     if payment_result.is_failure():
          return ApiResponse.not_found(payment_result.get_error_msg())
     
     payment = payment_result.get_data()  

     validate_result = PaymentService.validate_pending_payment_status(payment.status)
     if validate_result.is_failure():
          return ApiResponse.conflict(validate_result.get_error_msg())

     payment_complete = PaymentService.complete_payment(payment, request.data)

     payment_data = PaymentSerializer(payment_complete).data 
     return ApiResponse.ok(payment_data, 'Payments succesfully completed') 


@api_view(['PUT'])
def cancel_payment(request, payment_id):
     payment_result = PaymentService.get_payment_by_id(payment_id)
     if payment_result.is_failure():
          return ApiResponse.not_found(payment_result.get_error_msg())
     
     payment = payment_result.get_data()  

     validate_result = PaymentService.validate_pending_payment_status(payment.status)
     if validate_result.is_failure():
          return ApiResponse.conflict(validate_result.get_error_msg())

     PaymentService.update_payment_status(payment, 'cancelled')

     return ApiResponse.ok(None, 'Payments succesfully cancelled')
"""