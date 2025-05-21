from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.db import transaction

from tables.models import Table
from ..models import Reservation
from ..exceptions import (
    ReservationDateInvalid,
    ReservationHourInvalid,
    ReservationCustomerLimitExceeded,
    ReservationAlreadyCancelled,
    ReservationCannotChangeStatus
)

class ReservationService:
    OPENING_HOUR = 12  # 12:00 PM
    CLOSING_HOUR = 22  # 10:00 PM (Reservations up to 9:00 PM, meaning hour < 22)
    MAX_CUSTOMERS_PER_RESERVATION = 8

    @staticmethod
    def _validate_reservation_date(reservation_date: datetime) -> None:
        """
        Validates the reservation date and time constraints.
        """
        now = timezone.now()
        max_date_allowed = now + relativedelta(months=1)

        if reservation_date.replace(second=0, microsecond=0) < now.replace(second=0, microsecond=0):
            raise ReservationDateInvalid("Reservations must be made for a future date and time.")

        if reservation_date.date() == now.date():
             raise ReservationDateInvalid("Same day reservations are not allowed.")

        if reservation_date > max_date_allowed:
            raise ReservationDateInvalid("Reservations can only be made up to one month in advance.")

    @staticmethod
    def _validate_reservation_hour(reservation_date: datetime) -> None:
        """
        Validates the reservation hour against opening and closing times.
        """
        reservation_hour = reservation_date.hour
        if not (ReservationService.OPENING_HOUR <= reservation_hour < ReservationService.CLOSING_HOUR):
            raise ReservationHourInvalid(
                f"Reservations can only be scheduled between {ReservationService.OPENING_HOUR}:00 and {ReservationService.CLOSING_HOUR-1}:59."
            )

    @staticmethod
    def _validate_customer_limit(customer_number: int) -> None:
        """
        Validates the number of customers against the maximum allowed.
        """
        if customer_number > ReservationService.MAX_CUSTOMERS_PER_RESERVATION:
            raise ReservationCustomerLimitExceeded(
                f"Reservation can't be for more than {ReservationService.MAX_CUSTOMERS_PER_RESERVATION} customers."
            )

    @staticmethod
    def validate_new_reservation_data(
        name: str,
        email: str,
        phone_number: str,
        customer_number: int,
        reservation_date: datetime,
        table_id: int # Pass table_id or TableModel instance
    ) -> None:
        """
        Performs all necessary validations for creating a new reservation.
        """
        ReservationService._validate_reservation_date(reservation_date)
        ReservationService._validate_reservation_hour(reservation_date)
        ReservationService._validate_customer_limit(customer_number)

        # Further business logic for reservation creation could go here, e.g.,
        # checking table availability. This would involve querying the database.
        # Example:
        # if not TableModel.objects.filter(id=table_id, capacity__gte=customer_number).exists():
        #     raise SomeTableAvailabilityException("Table not available or too small for this number of customers.")
        # if Reservation.objects.filter(table_id=table_id, reservation_date=reservation_date, status__in=['BOOKED', 'ATTENDED']).exists():
        #     raise TableAlreadyBookedException("This table is already booked for this time.")

    @staticmethod
    def create_reservation(validated_data: dict) -> Reservation:
        """
        Creates a new reservation after all validations.
        """
        name = validated_data.get('name')
        email = validated_data.get('email')
        phone_number = validated_data.get('phone_number')
        customer_number = validated_data.get('customer_number')
        reservation_date = validated_data.get('reservation_date')
        table = validated_data.get('table')

        ReservationService.validate_new_reservation_data(
            name=name,
            email=email,
            phone_number=phone_number,
            customer_number=customer_number,
            reservation_date=reservation_date,
            table_id=table.id
        )

        with transaction.atomic():
            reservation = Reservation.objects.create(
                name=name,
                email=email,
                phone_number=phone_number,
                customer_number=customer_number,
                reservation_date=reservation_date,
                table=table,
                status=Reservation.STATUS_CHOICES[0][0] # Default to 'BOOKED' or 'PENDING' if you add it
            )
            return reservation

    @staticmethod
    def update_reservation(reservation: Reservation, validated_data: dict) -> Reservation:
        """
        Updates an existing reservation after validations.
        """
        for attr, value in validated_data.items():
            setattr(reservation, attr, value)

        # Only validate if the fields have changed or are part of critical domain logic
        if 'reservation_date' in validated_data:
            ReservationService._validate_reservation_date(reservation.reservation_date)
            ReservationService._validate_reservation_hour(reservation.reservation_date)
        if 'customer_number' in validated_data:
            ReservationService._validate_customer_limit(reservation.customer_number)

        with transaction.atomic():
            reservation.save()
            return reservation

    @staticmethod
    def cancel_reservation(reservation: Reservation) -> Reservation:
        """
        Cancels a reservation.
        """
        if reservation.status == Reservation.STATUS_CHOICES[4][0]: # 'CANCELLED'
            raise ReservationAlreadyCancelled("Reservation is already cancelled.")

        with transaction.atomic():
            reservation.status = Reservation.STATUS_CHOICES[4][0] # 'CANCELLED'
            reservation.cancelled_at = timezone.now()
            reservation.save()
            return reservation

    @staticmethod
    def attend_reservation(reservation: Reservation) -> Reservation:
        """
        Marks a reservation as attended.
        """
        if reservation.status == Reservation.STATUS_CHOICES[4][0]: # 'CANCELLED'
            raise ReservationCannotChangeStatus("Cannot mark a cancelled reservation as attended.")

        with transaction.atomic():
            reservation.status = Reservation.STATUS_CHOICES[2][0] # 'ATTENDED'
            reservation.save()
            return reservation

    @staticmethod
    def mark_reservation_not_attended(reservation: Reservation) -> Reservation:
        """
        Marks a reservation as not attended.
        """
        if reservation.status == Reservation.STATUS_CHOICES[4][0]: # 'CANCELLED'
            raise ReservationCannotChangeStatus("Cannot mark a cancelled reservation as not attended.")

        with transaction.atomic():
            reservation.status = Reservation.STATUS_CHOICES[3][0] # Set to 'NOT_ATTENDED'
            reservation.save()
            return reservation

    @staticmethod
    def assign_table_to_reservation(reservation: Reservation, table: Table) -> Reservation:
        """
        Assigns a table to a reservation.
        You might want to add business logic here like checking table availability.
        """
        with transaction.atomic():
            reservation.table = table
            reservation.save()
            return reservation