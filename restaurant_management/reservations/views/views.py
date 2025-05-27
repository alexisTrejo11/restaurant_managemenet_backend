import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from shared.response.django_response import DjangoResponseWrapper as ResponseWrapper
from ..serializers import ReservationSerializer
from ..services.reservation_service import ReservationService
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([AllowAny])
def request_user_reservation(request):
    user_id = getattr(request.user, 'id', 'Anonymous')
    logger.info(f"User {user_id} is requesting to create a reservation with data: {request.data}")

    try:
        serializer = ReservationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        reservation_created = ReservationService.create_reservation(
            validated_data=serializer.validated_data,
            is_admin=False
        )

        reservation_serialized = ReservationSerializer(reservation_created)
        logger.info(f"Reservation created successfully by user {user_id}. ID: {reservation_created.id}")

        return ResponseWrapper.success(
            data=reservation_serialized.data,
            message="Reservation Requested. To confirm your reservation, please check your email.",
        )
    except Exception as e:
        logger.error(f"Error creating reservation by user {user_id}: {str(e)}", exc_info=True)
        raise

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def get_today_reservations(request):
    user = request.user
    user_id = user.id
    logger.info(f"User {user_id} is requesting today's reservations")

    try:
        today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow = today + timedelta(days=2) - timedelta(microseconds=1)

        reservations = ReservationService.get_reservation_by_date_range(today, tomorrow)
        if len(reservations) == 0:
            return ResponseWrapper.success(data=[], message="No Reservations Were Scheduled Today")

        logger.info(f"User {user_id} retrieved {len(reservations)} reservations.")
        
        reservations_serialized = ReservationSerializer(reservations, many=True)
        return ResponseWrapper.success(
            data=reservations_serialized.data,
            message="Today's reservations retrieved successfully."
        )
    except Exception as e:
        logger.error(f"Error fetching today's reservations for user {user_id}: {str(e)}", exc_info=True)
        raise

@api_view(['PATCH'])
#@permission_classes([IsAuthenticated])
def update_status_reservation(request, reservation_id: int, new_status: str):
    user = request.user
    user_id = user.id
    new_status = new_status.upper()
    logger.info(f"User {user_id} is attempting to update reservation ID: {reservation_id} to status: {new_status}")

    if not new_status:
        logger.warning(f"User {user_id} tried to update reservation {reservation_id} without providing a status.")
        return ResponseWrapper.bad_request(message="Status is required")
        
    if not ReservationService.is_status_valid(new_status):
        logger.warning(f"User {user_id} provided an invalid status: {new_status} for reservation {reservation_id}.")
        return ResponseWrapper.bad_request(message="Invalid status")

    try:
        ReservationService.update_status_reservation(reservation_id, new_status)
        logger.info(f"Reservation {reservation_id} was successfully updated to status: {new_status} by user {user_id}.")
        
        return ResponseWrapper.success(message=f"Reservation Successfully Set As {new_status}")
    except Exception as e:
        logger.error(f"Error updating reservation {reservation_id} by user {user_id}: {str(e)}", exc_info=True)
        return ResponseWrapper.internal_server_error(message=str(e))

