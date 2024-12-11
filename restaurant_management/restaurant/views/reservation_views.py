"""
from rest_framework.response import Response
from restaurant.serializers import ReservationInsertSerializer, ReservationSerializer
from restaurant.services.reservation_service import ReservationService
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from datetime import datetime
from restaurant.utils.response import ApiResponse

@api_view(['GET'])
def get_reservation_by_id(request, reservation_id):
    reservation_result = ReservationService.get_reservation_by_id(reservation_id)

    if reservation_result.is_failure():
        return ApiResponse.not_found(reservation_result.get_error_msg())

    reservations_data = ReservationSerializer(reservation_result.get_data()).data
    return ApiResponse.ok(reservations_data, f'reservation with reservation Id {reservation_id} succesfully fetched')


@api_view(['GET'])
def get_reservations_by_email(request, email):
    reservation_result = ReservationService.get_reservations_by_email(email)

    if reservation_result.is_failure():
        return ApiResponse.not_found(reservation_result.get_error_msg())
    
    reservations_data = ReservationSerializer(reservation_result.get_data(), many=True).data
    return ApiResponse.ok(reservations_data, f'reservation with customer email {email} succesfully fetched')


@api_view(['GET'])
def get_reservations_by_date_range(request, start_date, end_date):
    reservations = ReservationService.get_reservations_by_date_range(start_date, end_date)
    
    reservations_data = ReservationSerializer(reservations, many=True).data
    return ApiResponse.ok(reservations_data, f'Reservation with data range {start_date}:{end_date} succesfully fetched')


@api_view(['GET'])
def get_today_reservations(request):
    reservations = ReservationService.get_today_reservations()
    
    reservations_data = ReservationSerializer(reservations, many=True).data
    return ApiResponse.ok(reservations_data, f'Today reservations succesfully fetched')


@api_view(['GET'])
def get_today_not_expired_reservations(request):
    reservations = ReservationService.get_today_not_expired_reservations()
    
    reservations_data = ReservationSerializer(reservations, many=True).data
    return ApiResponse.ok(reservations_data, f'Today(not expired) reservations succesfully fetched')


@api_view(['POST'])
def create_reservation(request):
        serializer = ReservationInsertSerializer(data=request.data)

        if serializer.is_valid() is False:
            return ApiResponse.bad_request(f'Validation failed:{serializer.errors}')

        reservation_result = ReservationService.create_reservation(request.data)        
        if reservation_result.is_failure():
            return ApiResponse.conflict(reservation_result.get_error_msg())

        reservation_data = ReservationSerializer(reservation_result.get_data()).data
        return ApiResponse.created(reservation_data, 'Reservation succesfully created')


@api_view(['DELETE'])
def delete_reservation_by_id(request, reservation_id):
    delete_result = ReservationService.delete_reservation_by_id(reservation_id)
    
    if delete_result.is_failure():
        return ApiResponse.not_found(delete_result.get_error_msg())

    return ApiResponse.ok(None, f'reservation with Id {reservation_id} succesfully deleted')
"""