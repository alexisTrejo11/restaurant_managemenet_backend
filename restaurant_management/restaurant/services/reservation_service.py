from restaurant.serializers import ReservationSerializer
from restaurant.models import Table, Reservation
from datetime import timedelta, datetime
from django.db.models import Q
from restaurant.utils.result import Result

class ReservationService:
    @staticmethod
    def create_reservation(data):
        reservation_time = data.get('reservation_time')
        customers_numbers = data.get('customers_numbers')

        if isinstance(reservation_time, str):
            reservation_time = datetime.fromisoformat(reservation_time)
        
        table_available = ReservationService._assign_table(reservation_time, customers_numbers)
        if table_available is None:
            return Result.error("No tables available for the requested time and number of customers.")
        
        reservation = Reservation(
            table= table_available,
            customer_name=data.get('customer_name'),
            customer_email=data.get('customer_email'),
            reservation_time=reservation_time,
            customers_numbers=customers_numbers,
        )

        reservation.save()

        return Result.success(reservation)


    @staticmethod
    def get_reservations_by_email(email):
        reservations = Reservation.objects.filter(customer_email=email)
        
        if len(reservations) == 0:
            return Result.error(f'Reservations with email:{email} not founded')

        return Result.success(reservations)


    @staticmethod
    def get_today_reservations():
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)

        return ReservationService._get_reservations_by_date_range(start_date, end_date)


    @staticmethod
    def get_today_not_expired_reservations():
        # Reduce the time 30 minutes cause is the max tolerance delay to apply the reservations
        start_date = datetime.now() - timedelta(minutes=30)
        end_date = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)

        return ReservationService._get_reservations_by_date_range(start_date, end_date)


    @staticmethod
    def get_reservation_by_id(reservation_id):
        try:
            reservation = Reservation.objects.get(pk=reservation_id) 

            return Result.success(reservation)
        except Reservation.DoesNotExist:
            return Result.error(f'reservation with Id {reservation_id} not found')


    @staticmethod
    def delete_reservation_by_id(reservation_id):
        try:
            reservation = Reservation.objects.get(id=reservation_id) 
            reservation.delete()
            
            return Result.success(None)
        except Reservation.DoesNotExist:
            return Result.error(f'reservation with Id {reservation_id} not found')


    @staticmethod
    def _get_reservations_by_date_range(start_date, end_date):
        if isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date)
        elif isinstance(end_date, str):
            end_date = datetime.fromisoformat(end_date)
        
        return Reservation.objects.filter(reservation_time__range=(start_date, end_date))


    @staticmethod
    def _assign_table(reservation_time, customers_numbers):
        # Define the time range (2.5 hours before and after the requested time)
        start_time = reservation_time - timedelta(hours=2, minutes=30)
        end_time = reservation_time + timedelta(hours=2, minutes=30)

        # Filter tables with enough seats, ordered by seat count (ascending)
        possible_tables = Table.objects.filter(seats__gte=customers_numbers).order_by('seats')

        for table in possible_tables:
            # Check if this table is free within the time range
            conflicting_reservations = Reservation.objects.filter(
                Q(table=table) & Q(reservation_time__range=(start_time, end_time))
            )

            if not conflicting_reservations.exists():
                return table

        return None