from rest_framework.decorators import api_view
from dependency_injector.wiring import inject, Provide

# Use Cases
from reservations.application.use_case.reservation_use_case import (
    GetReservationsByDateRangeUseCase,
    GetTodaysReservationUseCase,
    RequestReservationUseCase,
    UpdateReservationUseCase,
    CancelReservationUseCase,
)

# Container
from core.injector.reservation_container import ReservationContainer

# Utils & Serializers
from core.utils.dateTimeHandler import DateTimeHandler
from core.response.django_response import DjangoResponseWrapper
from ..serializers.reresvation_serializers import ReservationInsertSerializer, ReservationUpdateSerializer


@api_view(['GET'])
@inject
def get_reservations_by_date_range(
    request,
    use_case: GetReservationsByDateRangeUseCase = Provide[ReservationContainer.get_reservation_by_date_range]
):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    if not start_date_str or not end_date_str:
        return DjangoResponseWrapper.bad_request({
            "[error] Both start_date and end_date parameters are required.  " +
            "[example] /api/reservations?start_date=2023-05-01&end_date=2023-05-31"
        })

    try:
        start_date = DateTimeHandler.parse_date_to_ISO_8601(start_date_str)
        end_date = DateTimeHandler.parse_date_to_ISO_8601(end_date_str)
    except ValueError as e:
        return DjangoResponseWrapper.bad_request({"error": f"Invalid date format: {str(e)}"})

    reservations = use_case.execute(start_date, end_date)

    if not reservations:
        return DjangoResponseWrapper.success(
            data=[],
            message="No reservations found with the given search criteria."
        )

    return DjangoResponseWrapper.found(
        data=reservations,
        entity="Reservations"
    )


@api_view(['GET'])
@inject
def today_list(
    request,
    use_case: GetTodaysReservationUseCase = Provide[ReservationContainer.get_today_reservations]
):
    reservations = use_case.execute()

    if not reservations:
        return DjangoResponseWrapper.success(
            data=[],
            message="No reservations have been scheduled today."
        )

    return DjangoResponseWrapper.found(
        data=reservations,
        entity="Reservations"
    )


@api_view(['POST'])
@inject
def schedule_reservation(
    request,
    use_case: RequestReservationUseCase = Provide[ReservationContainer.request_reservation]
):
    serializer = ReservationInsertSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    reservation = use_case.execute(serializer.validated_data)

    return DjangoResponseWrapper.success(
        data=reservation.to_dict(),
        message="Reservation successfully scheduled."
    )


@api_view(['PUT'])
@inject
def update_reservation(
    request,
    reservation_id: str,
    use_case: UpdateReservationUseCase = Provide[ReservationContainer.update_reservation]
):
    serializer = ReservationUpdateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    updated_reservation = use_case.execute(serializer.validated_data, reservation_id)

    return DjangoResponseWrapper.updated(
        data=updated_reservation.to_dict(),
        entity="Reservation"
    )


@api_view(['DELETE'])
@inject
def cancel_reservation(
    request,
    request_id: str,
    use_case: CancelReservationUseCase = Provide[ReservationContainer.cancel_reservation]
):
    use_case.execute(request_id)

    return DjangoResponseWrapper.success(
        message="Reservation successfully cancelled."
    )
