from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from restaurant.services.domain.table import Table
from typing import Optional
from restaurant.utils.result import Result

class Reservation:
    class Status:
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

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def email(self):
        return self.__email

    @property
    def phone_number(self):
        return self.__phone_number

    @property
    def customer_number(self):
        return self.__customer_number

    @property
    def reservation_date(self):
        return self.__reservation_date

    @reservation_date.setter
    def reservation_date(self, value: datetime):
        self.__reservation_date = value

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value: str):
        self.__status = value

    @property
    def table(self):
        return self.__table

    @table.setter
    def table(self, value: Table):
        self.__table = value

    @property
    def created_at(self):
        return self.__created_at

    @property
    def cancelled_at(self):
        return self.__cancelled_at

    def __str__(self):
        return f"{self.__name} - {self.__reservation_date}"

    def cancel(self):
        if self.__status == self.Status.CANCELLED:
            raise ValueError("Reservation is already cancelled.")
        self.__status = self.Status.CANCELLED
        self.__cancelled_at = datetime.now()

    def attend(self):
        if self.__status == self.Status.CANCELLED:
            raise ValueError("Cannot mark a cancelled reservation as attended.")
        self.__status = self.Status.ATTENDED

    def mark_not_attended(self):
        if self.__status == self.Status.CANCELLED:
            raise ValueError("Cannot mark a cancelled reservation as not attended.")
        self.__status = self.Status.NOT_ATTENDED

    def assign_table(self, table: Table):
        self.__table = table

    def validate_date(self) -> Result:
        reservation_date = self.__reservation_date

        now = datetime.now()
        max_date_allowed = now + relativedelta(months=1)

        if reservation_date < now:
            return Result.error("Reservations must be made for a future date.")
        
        if reservation_date.date() == now.date():
            return Result.error("Same day reservations are not allowed.")

        if reservation_date > max_date_allowed:
            return Result.error("Reservations can only be made up to one month in advance.")

        return Result.success(None)

    def validate_hour(self):
        reservation_hour = self.__reservation_date.hour
        OPENING_HOUR = 12  # 12:00 PM
        CLOSING_HOUR = 22  # 10:00 PM

        if not (OPENING_HOUR <= reservation_hour < CLOSING_HOUR):
            return Result.error("Reservations can only be scheduled between 12:00 PM and 9:00 PM.")

        return Result.success(None)

    def validate_customer_limit(self) -> Result:
        if self.__customer_number > 8:
            return Result.error("Reservation can't be above 8 customers")

        return Result.success(None)
