from injector import inject
from ...domain.entities.reservation import Reservation
from orders.core.domain.entities.table_entity import Table
from orders.core.repositories.table_repository import TableRepository
from datetime import datetime
from core.exceptions.custom_exceptions import BusinessRuleViolationException
from typing import List

class ReservationService:
    @inject
    def __init__(self, reservation_repository, table_repository: TableRepository):
        self.reservation_repository = reservation_repository
        self.table_repository = table_repository
    
    def get_all(self):
        reservations = self.reservation_repository.get_all()
        return reservations

    def get_by_id(self, id):
        if reservation is None:
            reservation = self.reservation_repository.get_by_id(id)
        
        return reservation

    def get_by_filter(self, filter, value):
        if reservations is None:
            if filter == "email":
                reservations = self.reservation_repository.get_by_email(value)
            elif filter == "phone_number":
                reservations = self.reservation_repository.get_by_phone_number(value)
            elif filter == "name":
                reservations = self.reservation_repository.get_by_name(value)
            elif filter == "table":
                reservations = self.reservation_repository.get_by_table(value)
            else:
                raise ValueError("Invalid Filter")

        return reservations

    def get_by_time_range(self, start: datetime, end: datetime):
        if start > end:
            raise ValueError("Start_date must be before or equal to end_date")

        reservations = self.reservation_repository.get_reservations_by_date_range(start, end)
        
        return reservations
    
    def create(self, reservation: Reservation) -> Reservation:            
        reservation.validate_fields()
        
        created_reservation = self.reservation_repository.save(reservation)
        return created_reservation
    
    def cancel(self, reservation: Reservation) -> Reservation:            
        reservation.validate_fields()
        reservation.cancel()        

        self.reservation_repository.save(reservation)
        
    def update(self, incoming_changes: dict, existing_reservation: Reservation):
        existing_reservation.update(incoming_changes)
        
        return self.reservation_repository.save(existing_reservation, incoming_changes)
        
    def assign_table(self, reservation: Reservation) -> Reservation:
        suitable_tables = self.__find_suitable_tables(reservation.customer_number)
        if not suitable_tables:
            raise BusinessRuleViolationException("No suitable tables available for the requested number of customers.")
        
        available_table = self.__search_for_the_best_table(suitable_tables, reservation)

        reservation.assing_table(available_table)

        return reservation

    def delete_by_id(self, id):
        self.reservation_repository.delete(id)

    def __find_suitable_tables(self, party_size) -> List[Table]:
        all_tables = self.table_repository.get_all()

        suitables_tables = []
        for table in all_tables:
            if table.capacity >= party_size:
                suitables_tables.append(table)

        return sorted(
            suitables_tables, 
            key=lambda table: table.capacity
        )
        
    def __search_for_the_best_table(self, suitable_tables : List[Table], reservation : Reservation) -> Table:
        for table in suitable_tables:
            reservation_conflict = self.reservation_repository.get_by_table_and_reservation_time(
                table.number,
                reservation.reservation_date
            )

            if not reservation_conflict: 
                return table
            
        raise BusinessRuleViolationException("No tables available for the requested date and customer capacity.")
            
