from datetime import datetime
from core.mappers.table_mappers import TableMappers
from ...domain.entities.reservation import Reservation
from ...infrastructure.models.reservation_model import ReservationModel
from ...application.dto.reservation_dto import ReservationDTO

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
    def dict_to_domain(reservation_data: dict):
        reservation_date_str = reservation_data.get('reservation_date')

        try:
            reservation_date = datetime.strptime(reservation_date_str, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            raise ValueError("Invalid date format. Please use the correct format: YYYY-MM-DDTHH:MM:SS")

        return Reservation(
            name=reservation_data.get('name'),
            email=reservation_data.get('email'),
            phone_number=reservation_data.get('phone_number'),
            customer_number=reservation_data.get('customer_number'),
            reservation_date=reservation_date,
        )
    
    @staticmethod
    def to_dto(domain: Reservation) -> ReservationDTO:
        """
        Convierte una entidad de dominio `Reservation` al DTO `ReservationDTO`.
        """
        return ReservationDTO(
            id=domain.id,
            name=domain.name,
            email=domain.email,
            phone_number=domain.phone_number,
            customer_number=domain.customer_number,
            reservation_date=domain.reservation_date,
            status=domain.status,
            table=TableMappers.to_dto(domain.table) if domain.table else None,
            created_at=domain.created_at,
            cancelled_at=domain.cancelled_at
        )