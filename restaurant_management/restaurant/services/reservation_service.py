from restaurant.serializers import ReservationSerializer
from restaurant.utils.result import Result
from restaurant.repository.reservation_repository import ReservationRepository
from restaurant.repository.table_respository import TableRepository
from restaurant.services.domain.reservation import Reservation
from datetime import datetime, timedelta
from restaurant.utils.exceptions import DomainException

class ReservationService:
    def __init__(self):
        self.reservation_repository = ReservationRepository()
        self.table_repository = TableRepository()


    def get_all(self):
        return self.reservation_repository.get_all()


    def get_by_id(self, id):
        self.reservation_repository.get_by_id(id)


    def get_by_filter(self, filter, value):
        if filter == "email":
        	return self.reservation_repository.get_by_email(value)
        elif filter == "phone_number":
            return self.reservation_repository.get_by_phone_number(value)
        elif filter == "name":
            return self.reservation_repository.get_by_name(value)
        elif filter == "table":
            return self.reservation_repository.get_by_table(value)
        else:
            raise ValueError("Invalid Filter")


    def get_by_time_range(self, start : datetime, end : datetime):
        return self.reservation_repository.get_reservations_by_date_range(start, end)


    def validate_creation(self, reservation : Reservation) -> Result:
        date_result = reservation.validate_date()
        if date_result.is_failure():
            return date_result

        customer_result = reservation.validate_customer_limit()
        if customer_result.is_failure():
            return customer_result
    

    def create(self, reservation : Reservation) -> Reservation:
        suitable_tables = self._find_suitable_tables(reservation.customer_number)
        if not suitable_tables:
            raise DomainException("No suitable tables available for the requested number of customers.")


        for table in suitable_tables:
            reservation_conflict = self.reservation_repository.get_by_table_and_reservation_time(
                table,
                reservation.reservation_date
            )
            if not reservation_conflict: 
                reservation.assign_table(table) 
                self.reservation_repository.create(reservation)
                return reservation  

        raise DomainException("No tables available for the requested date and customer capacity.")


    def delete_by_id(self, id):
        return self.reservation_repository.delete(id)


    def _find_suitable_tables(self, party_size):
        all_tables = self.table_repository.get_all()

        suitables_tables = []
        for table in alltables:
            if table.capacity >= party_size:
                suitables_tables.append(table)

        return sorted(
            suitable_tables, 
            key=lambda table: table.capacity
        )
        