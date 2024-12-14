from restaurant.serializers import ReservationInsertSerializer, ReservationSerializer
from restaurant.services.reservation_service import ReservationService
from restaurant.utils.response import ApiResponse
from rest_framework.viewsets import ViewSet
from datetime import datetime, timedelta, date


class ReservationViews(ViewSet):
    def __init__(self):
        self.reservation_service = ReservationService()

    def getReservationById(self, request, pk):
        reservation = self.reservation_service.get_by_id(pk)
        if reservation is None:
            return ApiResponse.not_found("Reservation", 'ID', pk)

        reservations_data = ReservationSerializer(reservation_result.get_data()).data
        
        return ApiResponse.ok(reservations_data, f'reservation with reservation Id {reservation_id} succesfully fetched')


    def getReservationsByFilter(self, request, filter, value):
        filter_param = request.GET.get('filter')  
        value = request.GET.get('value')

        if not filter_param or not value:
            return ApiResponse.bad_request("Invalid URL param format")


        reservation = self.reservation_service.get_by_filter(email)
        if reservation is None:
            return ApiResponse.not_found("Reservation", filter, value)

        reservations_serialized = ReservationSerializer(reservation).data
        return ApiResponse.found(reservations_data, "reservation", filter, value)


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

        if not start or not end:
            start = today.replace(hour=0, minute=0, second=0, microsecond=0)
            end = today.replace(hour=23, minute=59, second=59, microsecond=999999)

        try:
            start_date = datetime.strptime(start, "%Y-%m-%d")
            end_date = datetime.strptime(end, "%Y-%m-%d")
        except ValueError as e:
            raise ValueError(f"Invalid date format: {e}")

        reservations = self.reservation_service.get_by_time_range(start,end)
        reservations_serialized = ReservationSerializer(reservations, many=True).data

        return ApiResponse.ok(reservations_serialized, f"Reservation successfully fetched. Date Range: {start}-{end_date}")


    def create(self, request):
            serializer = ReservationInsertSerializer(data=request.data)
            if serializer.is_valid() is False:
                return ApiResponse.bad_request(f'Validation failed:{serializer.errors}')  


            validation_result = self.reservation_service.validate_creation(reservation)
            if validation_result.is_failure():
                return ApiResponse.bad_request(validation_result.get_error_msg())  

            reservation = self.reservation_service.assing_table(reservation)

            reservation = self.reservation_service.create(reservation)        
            reservation_serialized = ReservationSerializer(reservation).data

            return ApiResponse.created(reservation_serialized, 'Reservation succesfully created')


    def deleteReservationById(self, request, pk):
        is_delete = self.reservation_service.delete_by_id(pk)
        if not is_delete:
            return ApiResponse.not_found("Reservation", 'ID', pk)

        return ApiResponse.ok(reservations_data, f'reservation with reservation ID [{pk}] succesfully fetched')

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