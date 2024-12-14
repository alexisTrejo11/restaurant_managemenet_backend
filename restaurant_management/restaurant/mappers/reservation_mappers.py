from datetime import datetime
from restaurant.repository.models.models import ReservationModel 
from restaurant.services.domain.reservation import Reservation
from restaurant.services.domain.table import Table

class ReservationMapper:
    @staticmethod
    def to_domain(model: ReservationModel):
        return Reservation(
            id=model.id,
            name=model.name,
            email=model.email,
            phone_number=model.phone_number,
            customer_number=model.customer_number,
            table=Table(id=model.table.id, name=model.table.name), 
            reservation_date=model.reservation_date,
            status=model.status,
            created_at=model.created_at,
            cancelled_at=model.cancelled_at,
     )

    @staticmethod
    def to_model(domain: Reservation , model=None):
        if model is None:
            model = ReservationModel()

        model.first_name = domain.first_name
        model.last_name = domain.last_name
        model.table_id = domain.table.id
        model.reservation_date = domain.reservation_date
        model.status = domain.status
        model.created_at = domain.created_at or datetime.now()
        model.cancelled_at = domain.cancelled_at

        return model

    @staticmethod
    def to_model(serializer):
       return Reservation(
            id=serializer.get('id'),
            name=serializer.get('name'),
            email=serializer.get('email'),
            phone_number=serializer.get('phone_number'),
            customer_number=serializer.get('customer_number'),
            reservation_date=serializer.get('reservation_date'),
     )
