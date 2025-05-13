from datetime import datetime
from restaurant.models import ReservationModel 
from restaurant.services.domain.reservation import Reservation
from core.mappers.table_mappers import TableMappers

class ReservationMapper:
    @staticmethod
    def to_domain(model: ReservationModel):
        return Reservation(
            id=model.id,
            name=model.name,
            email=model.email,
            phone_number=model.phone_number,
            customer_number=model.customer_number,
            table=TableMappers.to_domain(model.table), 
            reservation_date=model.reservation_date,
            status=model.status,
            created_at=model.created_at,
            cancelled_at=model.cancelled_at,
     )

    @staticmethod
    def to_model(domain: Reservation , model=None):
        if model is None:
            model = ReservationModel()

        model.name = domain.name
        model.table = TableMappers.to_model(domain.table)
        model.reservation_date = domain.reservation_date
        model.status = domain.status
        model.email = domain.email
        model.phone_number = domain.phone_number
        model.customer_number = domain.customer_number
        model.created_at = domain.created_at or datetime.now()
        model.cancelled_at = domain.cancelled_at

        return model

    @staticmethod
    def serializer_to_domain(serializer):
        reservation_date_str = serializer.get('reservation_date')

        try:
            reservation_date = datetime.strptime(reservation_date_str, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            raise ValueError("Invalid date format. Please use the correct format: YYYY-MM-DDTHH:MM:SS")

        return Reservation(
            name=serializer.get('name'),
            email=serializer.get('email'),
            phone_number=serializer.get('phone_number'),
            customer_number=serializer.get('customer_number'),
            reservation_date=reservation_date,
        )