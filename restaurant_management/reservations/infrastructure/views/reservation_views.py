from core.utils.permission import RoleBasedPermission
from restaurant_management.core.utils.dateTimeHandler import DateTimeHandler
from ...application.use_case.reservation_use_case import (
    ScheduleReservationUseCase,
    GetReservationsByDateRangeUseCase,
    CancelReservationUseCase,
    GetTodaysReservationUseCase,
    UpdateReservationUseCase,
)
from injector import Injector
from core.injector.app_module import AppModule
from rest_framework.views import APIView
from core.response.django_response import DjangoResponseWrapper
from ..serializers.reresvation_serializers import ReservationInsertSerializer, ReservationUpdateSerializer
from datetime import datetime

container = Injector([AppModule()])

# TODO: Permissions
class ReservationViews(APIView):
    def __init__(self, **kwargs):
        self.get_reservation_by_date_range_use_case = container.get(GetReservationsByDateRangeUseCase)
        self.get_today_reservation_use_case = container.get(GetTodaysReservationUseCase)
        self.schedule_reservation_use_case = container.get(ScheduleReservationUseCase)
        self.update_reservation_use_case = container.get(UpdateReservationUseCase)
        self.cancel_reservation_use_case = container.get(CancelReservationUseCase)
        super().__init__(**kwargs)

    def get_by_date_range(self, request):
        start_date_str = request.GET.get('start_date')  
        end_date_str = request.GET.get('end_date')
    
        if not start_date_str or not end_date_str:
            raise DjangoResponseWrapper.bad_request({
                "[error] Both start_date and end_date parameters are required. "
                "[example] /api/reservations?start_date=2023-05-01&end_date=2023-05-31",
            })
        
        start_date = DateTimeHandler.parse_date_to_ISO_8601(start_date_str)
        end_date = DateTimeHandler.parse_date_to_ISO_8601(end_date)

        

        reservation = self.get_reservation_by_date_range_use_case.execute(start_date, end_date)
        if not reservation or len(reservation) == 0:
            return DjangoResponseWrapper.success(
                data=[],
                message="Reservation Not Found With Given Search Params"
                )

        return DjangoResponseWrapper.found(
            data=reservation,
            entity="Reservations"
        )

    def today_list(self, request):
        reservation = self.get_today_reservation_use_case.execute()
        if not reservation or len(reservation) == 0:
            return DjangoResponseWrapper.success(
                data=[],
                message="Any Reservation Have Been Scheduled Today",
                )

        return DjangoResponseWrapper.found(
            data=reservation,
            entity="Reservations"
        )
    
    def schedule(self, request):
        serializer = ReservationInsertSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        reservation = self.schedule_reservation_use_case.execute(serializer.data)

        return DjangoResponseWrapper.success(
            data=reservation.to_dict(),
            message="Reservation Successfully Scheduled on Requested DateTime",
        )
    
    def update(self, request, reservation_id):
        serializer = ReservationUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        reservation_update = self.update_reservation_use_case.execute(serializer.data, reservation_id)

        return DjangoResponseWrapper.updated(
            data=reservation_update.to_dict(),
            entity="Reservation",
        )        

    def cancel(self, request, request_id):
        self.cancel_reservation_use_case.execute(request_id)

        return DjangoResponseWrapper.success(
            message="Reservation Successfully Cancelled",
        )
