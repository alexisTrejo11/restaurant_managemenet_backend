from restaurant.serializers import ReservationSerializer
from restaurant.utils.result import Result
from restaurant.repository.reservation_repository import ReservationRepository
from restaurant.repository.table_respository import TableRepository
from restaurant.services.domain.reservation import Reservation
from datetime import datetime
from restaurant.utils.exceptions import DomainException
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

class ReservationService:
    def __init__(self):
        self.reservation_repository = ReservationRepository()
        self.table_repository = TableRepository()


    def get_all(self):
        reservations = cache.get('all_reservations')

        if reservations is None:
            reservations = self.reservation_repository.get_all()
            cache.set('all_reservations', reservations, timeout=3600)  
        
        return reservations


    def get_by_id(self, id):
        reservation = cache.get(f'reservation_{id}')
        
        if reservation is None:
            reservation = self.reservation_repository.get_by_id(id)
            cache.set(f'reservation_{id}', reservation, timeout=3600)
        
        return reservation


    def get_by_filter(self, filter, value):
        cache_key = f'reservations_{filter}_{value}'
        reservations = cache.get(cache_key)
        
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

            cache.set(cache_key, reservations, timeout=3600)
        return reservations


    def get_by_time_range(self, start: datetime, end: datetime):
        cache_key = f'reservations_time_range_{start.timestamp()}_{end.timestamp()}'
        reservations = cache.get(cache_key)

        if reservations is None:
            reservations = self.reservation_repository.get_reservations_by_date_range(start, end)
            cache.set(cache_key, reservations, timeout=3600)
        
        return reservations
    

    def validate_creation(self, reservation : Reservation) -> Result:
        date_result = reservation.validate_date()
        if date_result.is_failure():
            return Result.error(date_result.get_error_msg())
        
        hour_result = reservation.validate_hour()
        if hour_result.is_failure():
            return hour_result

        customer_result = reservation.validate_customer_limit()
        if customer_result.is_failure():
            return Result.error(customer_result.get_error_msg())
        
        return Result.success(None)

    
    def create(self, reservation: Reservation) -> Reservation:
        suitable_tables = self.__find_suitable_tables(reservation.customer_number)
        if not suitable_tables:
            logger.warning(f"No suitable tables available for {reservation.customer_number} customers.")
            raise DomainException("No suitable tables available for the requested number of customers.")

        for table in suitable_tables:
            reservation_conflict = self.reservation_repository.get_by_table_and_reservation_time(
                table,
                reservation.reservation_date
            )

            if not reservation_conflict: 
                reservation.assign_table(table) 
                
                created_reservation = self.reservation_repository.create(reservation)
                logger.info(f"Reservation created successfully with ID {created_reservation.id} for table {table.id}.")
                
                return created_reservation

        logger.warning(f"No tables available for the requested date {reservation.reservation_date} and customer capacity {reservation.customer_number}.")
        raise DomainException("No tables available for the requested date and customer capacity.")


    def delete_by_id(self, id):
        deleted = self.reservation_repository.delete(id)
        if deleted:
            logger.info(f"Reservation with ID {id} deleted successfully.")
        else:
            logger.warning(f"Failed to delete reservation with ID {id}.")
        return deleted


    def __find_suitable_tables(self, party_size):
        all_tables = self.table_repository.get_all()

        suitables_tables = []
        for table in all_tables:
            if table.capacity >= party_size:
                suitables_tables.append(table)

        return sorted(
            suitables_tables, 
            key=lambda table: table.capacity
        )
        