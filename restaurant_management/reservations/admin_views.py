from rest_framework import viewsets, status
from .models import Reservation
from core.response.django_response import DjangoResponseWrapper
from django.shortcuts import get_object_or_404
from .serializers import ReservationSerializer
import logging

logger = logging.getLogger(__name__)

# TODO: Add Filters
class ReservationAdminViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            queryset = Reservation.objects.all()
            serializer = ReservationSerializer(queryset, many=True)
            return DjangoResponseWrapper.found(
                data=serializer.data,
                entity="Reservation List",
            )
        except Exception as e:
            logger.error(f"Error listing reservations: {str(e)}", exc_info=True)
            return DjangoResponseWrapper.internal_server_error(message="Error retrieving reservation list.")
        
    def retrieve(self, request, pk=None):
        try:
            queryset = Reservation.objects.all()
            reservation = get_object_or_404(queryset, pk=pk)
            serializer = ReservationSerializer(reservation)
            return DjangoResponseWrapper.found(
                data=serializer.data,
                entity=f"Reservation {pk}",
            )
        except Exception as e:
            logger.error(f"Error retrieving reservation {pk}: {str(e)}", exc_info=True)
            return DjangoResponseWrapper.internal_server_error(message=f"Error retrieving reservation {pk}.")
    
    def create(self, request):
        serializer = ReservationSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            reservation_created = serializer.save() 
            return DjangoResponseWrapper.created(
                data=ReservationSerializer(reservation_created).data, 
                entity="Reservation"
            )
        except Exception as e:
            logger.error(f"Error creating reservation: {str(e)}", exc_info=True)
            return DjangoResponseWrapper.bad_request(message="Error creating reservation.", data=serializer.errors)


    def update(self, request, pk=None):
        try:
            queryset = Reservation.objects.all()
            existing_reservation = get_object_or_404(queryset, pk=pk)

            serializer = ReservationSerializer(existing_reservation, data=request.data, partial=False)
            serializer.is_valid(raise_exception=True)

            reservation_updated = serializer.save()
            return DjangoResponseWrapper.updated(
                data=ReservationSerializer(reservation_updated).data, 
                entity=f"Reservation {pk}"
            )
        except Exception as e:
            logger.error(f"Error updating reservation {pk}: {str(e)}", exc_info=True)
            return DjangoResponseWrapper.bad_request(message=f"Error updating reservation {pk}.", data=serializer.errors)


    def destroy(self, request, pk=None):
        try:
            queryset = Reservation.objects.all()
            reservation = get_object_or_404(queryset, pk=pk)

            reservation.delete()

            return DjangoResponseWrapper.deleted(f"Reservation {pk}")
        except Exception as e:
            logger.error(f"Error deleting reservation {pk}: {str(e)}", exc_info=True)
            return DjangoResponseWrapper.internal_server_error(message=f"Error deleting reservation {pk}.")