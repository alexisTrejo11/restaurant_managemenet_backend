from rest_framework.response import Response
from restaurant.serializers import ReservationInsertSerializer, ReservationSerializer
from restaurant.services.reservation_service import ReservationService
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from datetime import datetime

@api_view(['GET'])
def get_reservation_by_id(request, reservation_id):
    reservation = ReservationService.get_reservation_by_id(reservation_id)
    
    if reservation is None:
        return Response({'message': f'reservation with Id {reservation_id} not found'
        },status=status.HTTP_404_NOT_FOUND)

    return Response({
        'data' : reservation,
        'message' : f'reservation with Id {reservation_id} succesfully fetched'
    })


@api_view(['GET'])
def get_reservations_by_email(request, email):
    reservation = ReservationService.get_reservations_by_name(email)
    
    return Response({
        'data' : reservation,
        'message' : f'reservation with customer email {email} succesfully fetched'
    })


@api_view(['GET'])
def get_reservations_by_date_range(request, start_date, end_date):
    reservations = ReservationService.get_reservations_by_date_range(start_date, end_date)
    
    return Response({
        'data' : reservations,
        'message' : f'Reservation with data range {start_date}:{end_date} succesfully fetched'
    })


@api_view(['GET'])
def get_today_reservations(request):
    reservations = ReservationService.get_today_reservations()
    
    return Response({
        'data' : reservations,
        'message' : f'Today reservations succesfully fetched'
    })


@api_view(['GET'])
def get_today_not_expired_reservations(request):
    reservations = ReservationService.get_today_not_expired_reservations()
    
    return Response({
        'data' : reservations,
        'message' : f'Today(not expired) reservations succesfully fetched'
    })


@api_view(['POST'])
def create_reservation(request):
        serializer = ReservationInsertSerializer(data=request.data)
        if serializer.is_valid() is False:
            return  Response({
            'message' : f'Validation failed:{serializer.errors}'   
            }, status=status.HTTP_400_BAD_REQUEST)

        reservation_result = ReservationService.create_reservation(request.data)
        if reservation_result.is_failure():
            return  Response({
            'message' : reservation_result.get_error_msg(),
            }, status=status.HTTP_409_CONFLICT)

        return Response({
        'data' : reservation_result.get_data(),
        'message' : 'Reservation succesfully created'
        })

    
@api_view(['DELETE'])
def delete_reservation_by_id(request, reservation_id):
    is_reservation_delete = ReservationService.delete_reservation_by_id(reservation_id)
    
    if is_reservation_delete is False:
        return Response({'message': f'reservation with Id {reservation_id} not found'
        },status=status.HTTP_404_NOT_FOUND)

    return Response({
        'message' : f'reservation with Id {reservation_id} succesfully deleted'
    })


