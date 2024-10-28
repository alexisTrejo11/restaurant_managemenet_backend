from restaurant.serializers import ReservationSerializer
from restaurant.models import Table, Reservation
from datetime import timedelta, datetime
from django.db.models import Q
from restaurant.utils.result import Result
from restaurant.serializers import ReservationSerializer

class ReservationService:
    @staticmethod
    def create_reservation(data):
        reservation_time = data.get('reservation_time')
        customers_numbers = data.get('customers_numbers')

        if isinstance(reservation_time, str):
            reservation_time = datetime.fromisoformat(reservation_time)
        
        table_available = ReservationService.assign_table(reservation_time, customers_numbers)
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

        return Result.success(ReservationSerializer(reservation).data)


    @staticmethod
    def assign_table(reservation_time, customers_numbers):
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


    @staticmethod
    def get_reservations_by_name(email):
        try:
            reservations = Reservation.objects.filter(customer_email=email)
            reservations_serialized = ReservationSerializer(reservations, many=True)

            return reservations_serialized.data
        except Reservation.DoesNotExist:
            return None

    
    @staticmethod
    def get_reservations_by_date_range(start_date, end_date):
        if isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date)
        elif isinstance(end_date, str):
            end_date = datetime.fromisoformat(end_date)
        
        reservations = Reservation.objects.filter(reservation_time__range=(start_date, end_date))

        reservations_serialized = ReservationSerializer(reservations, many=True)
        return reservations_serialized.data


    @staticmethod
    def get_today_reservations():
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)

        reservations = ReservationService.get_reservations_by_date_range(start_date, end_date)
        
        reservations_serialized = ReservationSerializer(reservations, many=True)
        return reservations_serialized.data


    @staticmethod
    def get_today_not_expired_reservations():
        start_date = datetime.now() - timedelta(minutes=30)
        end_date = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)

        reservations = ReservationService.get_reservations_by_date_range(start_date, end_date)

        reservations_serialized = ReservationSerializer(reservations, many=True)
        return reservations_serialized.data

    @staticmethod
    def get_reservation_by_id(reservation_id):
        try:
            reservation = Reservation.objects.get(id=reservation_id) 
            reservation_serialized = ReservationSerializer(reservation)
            
            return reservation_serialized.data
        except Reservation.DoesNotExist:
            return None


    @staticmethod
    def delete_reservation_by_id(reservation_id):
        try:
            reservation = Reservation.objects.get(id=reservation_id) 
            reservation.delete()
            
            return True
        except Reservation.DoesNotExist:
            return False