import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from shared.response.django_response import DjangoResponseWrapper as ResponseWrapper
from ..serializers import ReservationSerializer
from ..services.reservation_service import ReservationService
from django.utils import timezone
from datetime import timedelta
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..documentation.reservation_doc_data import ReservationDocumentationData as ReservationDocData
from rest_framework import status

logger = logging.getLogger(__name__)

@swagger_auto_schema(
    method='post',
    operation_id='request_reservation',
    operation_summary=ReservationDocData.create_operation_summary,
    operation_description=ReservationDocData.create_operation_description,
    request_body=ReservationSerializer,
    responses={
        status.HTTP_200_OK: ReservationDocData.reservation_response,
        status.HTTP_400_BAD_REQUEST: ReservationDocData.validation_error_response,
        status.HTTP_500_INTERNAL_SERVER_ERROR: 'Internal server error'
    },
    tags=['Reservations']
)
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

@swagger_auto_schema(
    method='get',
    operation_id='get_today_reservations',
    operation_summary=ReservationDocData.today_operation_summary,
    operation_description=ReservationDocData.today_operation_description,
    responses={
        status.HTTP_200_OK: ReservationDocData.today_reservations_response,
        status.HTTP_401_UNAUTHORIZED: 'Unauthorized - Authentication required',
        status.HTTP_500_INTERNAL_SERVER_ERROR: 'Internal server error'
    },
    tags=['Reservations']
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
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

@swagger_auto_schema(
    method='patch',
    operation_id='update_reservation_status',
    operation_summary=ReservationDocData.update_status_operation_summary,
    operation_description=ReservationDocData.update_status_operation_description,
    manual_parameters=[
        openapi.Parameter(
            'new_status',
            openapi.IN_PATH,
            description="New status (PENDING/CONFIRMED/CANCELLED)",
            type=openapi.TYPE_STRING,
            required=True
        )
    ],
    responses={
        status.HTTP_200_OK: ReservationDocData.status_update_response,
        status.HTTP_400_BAD_REQUEST: ReservationDocData.invalid_status_response,
        status.HTTP_401_UNAUTHORIZED: 'Unauthorized - Authentication required',
        status.HTTP_404_NOT_FOUND: 'Reservation not found',
        status.HTTP_500_INTERNAL_SERVER_ERROR: 'Internal server error'
    },
    tags=['Reservations']
)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
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