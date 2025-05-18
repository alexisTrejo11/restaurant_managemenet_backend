from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from reservations.domain.entities.table import Table
from ..exceptions.expections import (
    ReservationDateInvalid,
    ReservationHourInvalid,
    ReservationCustomerLimitExceeded
)
from typing import Optional

class Reservation:
    class Status:
        PENDING = 'PENDING'
        BOOKED = 'BOOKED'
        ATTENDED = 'ATTENDED'
        NOT_ATTENDED = 'NOT_ATTENDED'
        CANCELLED = 'CANCELLED'

        CHOICES = [
            (BOOKED, 'Booked'),
            (ATTENDED, 'Attended'),
            (NOT_ATTENDED, 'Not Attended'),
            (CANCELLED, 'Cancelled'),
        ]

    def __init__(
        self,
        name: str,
        email: str,
        phone_number: str,
        customer_number: int,
        reservation_date: datetime,
        status: str = Status.BOOKED,
        table: Table = None,
        created_at: Optional[datetime] = None,
        cancelled_at: Optional[datetime] = None,
        id: Optional[int] = None,
    ):
        self.__id = id
        self.__name = name
        self.__email = email
        self.__phone_number = phone_number
        self.__customer_number = customer_number
        self.__reservation_date = reservation_date
        self.__status = status
        self.__table = table
        self.__created_at = created_at or datetime.now()
        self.__cancelled_at = cancelled_at

    def validate_fields(self):
        self.validate_date()
        self.validate_hour()
        self.validate_customer_limit()

    def cancel(self):
        if self.__status == self.Status.CANCELLED:
            raise ReservationDateInvalid("Reservation is already cancelled.")
        self.__status = self.Status.CANCELLED
        self.__cancelled_at = datetime.now()

    def attend(self):
        if self.__status == self.Status.CANCELLED:
            raise ReservationDateInvalid("Cannot mark a cancelled reservation as attended.")
        self.__status = self.Status.ATTENDED

    def mark_not_attended(self):
        if self.__status == self.Status.CANCELLED:
            raise ReservationDateInvalid("Cannot mark a cancelled reservation as not attended.")
        self.__status = self.Status.NOT_ATTENDED

    def assign_table(self, table: Table):
        self.__table = table

    def validate_date(self) -> None:
        reservation_date = self.__reservation_date
        now = datetime.now()
        max_date_allowed = now + relativedelta(months=1)

        if reservation_date < now:
            raise ReservationDateInvalid("Reservations must be made for a future date.")

        if reservation_date.date() == now.date():
            raise ReservationDateInvalid("Same day reservations are not allowed.")

        if reservation_date > max_date_allowed:
            raise ReservationDateInvalid("Reservations can only be made up to one month in advance.")

    def validate_hour(self) -> None:
        reservation_hour = self.__reservation_date.hour
        OPENING_HOUR = 12  # 12:00 PM
        CLOSING_HOUR = 22  # 10:00 PM

        if not (OPENING_HOUR <= reservation_hour < CLOSING_HOUR):
            raise ReservationHourInvalid("Reservations can only be scheduled between 12:00 PM and 9:00 PM.")

    def validate_customer_limit(self) -> None:
        if self.__customer_number > 8:
            raise ReservationCustomerLimitExceeded("Reservation can't be above 8 customers")
        
    def update(self, incoming_changes: dict):
        if 'name' in incoming_changes:
            self.__name = incoming_changes['name'] if incoming_changes['name'] else self.__name
        if 'email' in incoming_changes:
            self.__email = incoming_changes['email'] if incoming_changes['email'] else self.__email
        if 'phone_number' in incoming_changes:
            self.__phone_number = incoming_changes['phone_number'] if incoming_changes['phone_number'] else self.__phone_number
        if 'customer_number' in incoming_changes:
            self.__customer_number = incoming_changes['customer_number']
            self._validate_customer_limit()