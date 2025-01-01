from tkinter.tix import Tree
from restaurant.serializers import ReservationInsertSerializer, ReservationSerializer
from restaurant.services.reservation_service import ReservationService
from restaurant.utils.response import ApiResponse
from rest_framework.viewsets import ViewSet
from datetime import datetime, timedelta, date
from restaurant.mappers.reservation_mappers import ReservationMapper


class ReservationViews(ViewSet):
    def __init__(self):
        self.reservation_service = ReservationService()

    def getReservationById(self, request, id):
        reservation = self.reservation_service.get_by_id(id)
        if reservation is None:
            return ApiResponse.not_found("Reservation", 'ID', id)

        reservations_data = ReservationSerializer(reservation).data
        
        return ApiResponse.ok(reservations_data, f'reservation with reservation Id {id} succesfully fetched')


    def getReservationsByFilter(self, request):
        filter_param = request.GET.get('filter')  
        value = request.GET.get('value')

        if not filter_param or not value:
            return ApiResponse.bad_request("Invalid URL param format")

        reservation = self.reservation_service.get_by_filter(filter_param, value)
        if reservation is None:
            return ApiResponse.not_found("Reservation", filter_param, value)

        reservations_data = ReservationSerializer(reservation, many=True).data
        return ApiResponse.found(reservations_data, "reservation", filter_param, value)


    def getTodayReservation(self, request):
        today = datetime.now()

        start = today.replace(hour=0, minute=0, second=0, microsecond=0)
        end = today.replace(hour=23, minute=59, second=59, microsecond=999999)

        reservations = self.reservation_service.get_by_time_range(start,end)
        reservations_serialized = ReservationSerializer(reservations, many=True).data

        return ApiResponse.ok(reservations_serialized, f"Today's reservation successfully fetched. Today Date: {today.date()}")


    def getReservationByDateRange(self, request):
        start = request.GET.get('start')
        end = request.GET.get('end')
        today = datetime.now()


        if not start or not end:
            start = today.replace(hour=0, minute=0, second=0, microsecond=0)
            end = today.replace(hour=23, minute=59, second=59, microsecond=999999)

        try:
            start_date = datetime.strptime(start, "%Y-%m-%d")
            end_date = datetime.strptime(end, "%Y-%m-%d")
        except ValueError as e:
            raise ValueError(f"Invalid date format: {e}")

        reservations = self.reservation_service.get_by_time_range(start_date,end_date)
        reservations_serialized = ReservationSerializer(reservations, many=True).data

        return ApiResponse.ok(reservations_serialized, f"Reservation successfully fetched. Date Range: {start}-{end_date}")


    def create(self, request):
            serializer = ReservationInsertSerializer(data=request.data)
            if serializer.is_valid() is False:
                return ApiResponse.bad_request(f'Validation failed:{serializer.errors}')  

            new_reservation = ReservationMapper.serializer_to_domain(serializer.data)

            validation_result = self.reservation_service.validate_creation(new_reservation)
            if validation_result.is_failure():
                return ApiResponse.bad_request(validation_result.get_error_msg())  

            reservation_created = self.reservation_service.create(new_reservation)        
            reservation_serialized = ReservationSerializer(reservation_created).data

            return ApiResponse.created(reservation_serialized, 'Reservation succesfully created')


    def deleteById(self, request, pk):
        is_delete = self.reservation_service.delete_by_id(pk)
        if not is_delete:
            return ApiResponse.not_found("Reservation", 'ID', pk)

        return ApiResponse.deleted('Reservation')

"""

    def get_reservations_by_email(self, request, email):
        reservation_result = ReservationService.get_reservations_by_email(email)

        if reservation_result.is_failure():
            return ApiResponse.not_found(reservation_result.get_error_msg())
        
        reservations_data = ReservationSerializer(reservation_result.get_data(), many=True).data
        return ApiResponse.ok(reservations_data, f'reservation with customer email {email} succesfully fetched')


    def get_reservations_by_date_range(request, start_date, end_date):
        reservations = ReservationService.get_reservations_by_date_range(start_date, end_date)
        
        reservations_data = ReservationSerializer(reservations, many=True).data
        return ApiResponse.ok(reservations_data, f'Reservation with data range {start_date}:{end_date} succesfully fetched')


    def get_today_reservations(self, request):
        reservations = ReservationService.get_today_reservations()
        
        reservations_data = ReservationSerializer(reservations, many=True).data
        return ApiResponse.ok(reservations_data, f'Today reservations succesfully fetched')


    def get_today_not_expired_reservations(self, request):
        reservations = ReservationService.get_today_not_expired_reservations()
        
        reservations_data = ReservationSerializer(reservations, many=True).data
        return ApiResponse.ok(reservations_data, f'Today(not expired) reservations succesfully fetched')
"""