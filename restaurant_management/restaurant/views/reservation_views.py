from restaurant.serializers import ReservationInsertSerializer, ReservationSerializer
from restaurant.services.reservation_service import ReservationService
from restaurant.utils.response import ApiResponse
from rest_framework.viewsets import ViewSet
from datetime import datetime
from restaurant.mappers.reservation_mappers import ReservationMapper
from restaurant.injector.app_module import AppModule
from injector import Injector
from drf_yasg.utils import swagger_auto_schema
from restaurant.utils.permission import RoleBasedPermission


container = Injector([AppModule()])

class ReservationViews(ViewSet):
    # Role Permissions
    def get_permissions(self):
        if self.action in ['get_today_reservation']:
             return [RoleBasedPermission(['admin', 'staff'])]
        elif self.action in ['delete_reservation_by_id', 'get_reservations_by_filter', 'get_reservation_by_id']:
             return [RoleBasedPermission(['admin'])]
    
    # Reservation Service injection
    def get_reservation_service(self):
        return container.get(ReservationService)

    @swagger_auto_schema(
        operation_description="Get reservation by ID",
        responses={
            200: ReservationSerializer,
            404: "Reservation not found"
        }
    )
    def get_reservation_by_id(self, request, reservation_id):
        reservation_service = self.get_reservation_service()

        reservation = reservation_service.get_by_id(reservation_id)
        if reservation is None:
            return ApiResponse.not_found("Reservation", 'ID', reservation_id)

        reservations_data = ReservationSerializer(reservation).data
        
        return ApiResponse.ok(reservations_data, f'Reservation with reservation Id {reservation_id} successfully fetched')


    @swagger_auto_schema(
        operation_description="Get reservations by filter",
        responses={
            200: ReservationSerializer(many=True),
            400: "Invalid URL param format",
            404: "Reservations not found"
        }
    )
    def get_reservations_by_filter(self, request):
        reservation_service = self.get_reservation_service()

        filter_param = request.GET.get('filter')  
        value = request.GET.get('value')

        if not filter_param or not value:
            return ApiResponse.bad_request("Invalid URL param format")

        reservation = reservation_service.get_by_filter(filter_param, value)
        if reservation is None:
            return ApiResponse.not_found("Reservation", filter_param, value)

        reservations_data = ReservationSerializer(reservation, many=True).data
        return ApiResponse.found(reservations_data, "Reservation", filter_param, value)


    @swagger_auto_schema(
        operation_description="Get today's reservations",
        responses={
            200: ReservationSerializer(many=True),
        }
    )
    def get_today_reservation(self, request):
        reservation_service = self.get_reservation_service()

        today = datetime.now()
        start = today.replace(hour=0, minute=0, second=0, microsecond=0)
        end = today.replace(hour=23, minute=59, second=59, microsecond=999999)

        reservations = reservation_service.get_by_time_range(start, end)
        reservations_serialized = ReservationSerializer(reservations, many=True).data

        return ApiResponse.ok(reservations_serialized, f"Today's reservation successfully fetched. Today Date: {today.date()}")


    @swagger_auto_schema(
        operation_description="Get reservations by date range",
        responses={
            200: ReservationSerializer(many=True),
            400: "Invalid date format",
        }
    )
    def get_reservation_by_date_range(self, request):
        reservation_service = self.get_reservation_service()

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
            return ApiResponse.bad_request(f"Invalid date format: {e}")

        reservations = reservation_service.get_by_time_range(start_date, end_date)
        reservations_serialized = ReservationSerializer(reservations, many=True).data

        return ApiResponse.ok(reservations_serialized, f"Reservation successfully fetched. Date Range: {start}-{end_date}")


    @swagger_auto_schema(
        operation_description="Create a reservation",
        request_body=ReservationInsertSerializer,
        responses={
            201: ReservationSerializer,
            400: "Validation failed or Invalid data",
        }
    )
    def create_reservation(self, request):
        reservation_service = self.get_reservation_service()
            
        serializer = ReservationInsertSerializer(data=request.data)
        if serializer.is_valid() is False:
            return ApiResponse.bad_request(f'Validation failed: {serializer.errors}')  

        new_reservation = ReservationMapper.serializer_to_domain(serializer.data)

        validation_result = reservation_service.validate_creation(new_reservation)
        if validation_result.is_failure():
            return ApiResponse.bad_request(validation_result.get_error_msg())  

        reservation_created = reservation_service.create(new_reservation)        
        reservation_serialized = ReservationSerializer(reservation_created).data

        return ApiResponse.created(reservation_serialized, 'Reservation successfully created')


    @swagger_auto_schema(
        operation_description="Delete reservation by ID",
        responses={
            200: "Reservation successfully deleted",
            404: "Reservation not found"
        }
    )
    def delete_reservation_by_id(self, request, reservation_id):
        reservation_service = self.get_reservation_service()

        is_deleted = reservation_service.delete_by_id(reservation_id)
        if not is_deleted:
            return ApiResponse.not_found("Reservation", 'ID', reservation_id)

        return ApiResponse.deleted('Reservation')
