from ...domain.entities.reservation import Reservation
from ...infrastructure.models.reservation_model import ReservationModel
from ...application.repositories.reservation_repository import ReservationRepository
from ...application.mappers.table_mapper import ReservationMapper

from datetime import datetime
from typing import List, Optional

class DjangoReservationRepository(ReservationRepository):
    def get_all(self) -> List[Reservation]:
        models = ReservationModel.objects.all()
        return [ReservationMapper.model_to_domain(model) for model in models]

    def get_by_id(self, reservation_id: int) -> Optional[Reservation]:
        try:
            model = ReservationModel.objects.get(id=reservation_id)
            return ReservationMapper.model_to_domain(model)
        except ReservationModel.DoesNotExist:
            return None

    def get_by_email(self, email: str) -> List[Reservation]:
        models = ReservationModel.objects.filter(email=email)
        return [ReservationMapper.model_to_domain(model) for model in models]

    def get_by_phone_number(self, phone_number: str) -> List[Reservation]:
        models = ReservationModel.objects.filter(phone_number=phone_number)
        return [ReservationMapper.model_to_domain(model) for model in models]

    def get_by_name(self, name: str) -> List[Reservation]:
        models = ReservationModel.objects.filter(name__icontains=name)
        return [ReservationMapper.model_to_domain(model) for model in models]

    def get_by_table(self, table_number: int) -> List[Reservation]:
        models = ReservationModel.objects.filter(table_id=table_number)
        return [ReservationMapper.model_to_domain(model) for model in models]

    def get_reservations_by_date_range(self, start: datetime, end: datetime) -> List[Reservation]:
        models = ReservationModel.objects.filter(reservation_date__range=(start, end))
        return [ReservationMapper.model_to_domain(model) for model in models]

    def get_by_table_and_reservation_time(self, table_number: int, reservation_date: datetime) -> Optional[Reservation]:
        try:
            model = ReservationModel.objects.get(
                table_id=table_number,
                reservation_date=reservation_date
            )
            return ReservationMapper.model_to_domain(model)
        except ReservationModel.DoesNotExist:
            return None

    def save(self, reservation: Reservation) -> Reservation:
        model = ReservationMapper.domain_to_model(reservation)
        model.save()
        return ReservationMapper.model_to_domain(model)

    def delete(self, reservation_id: int) -> None:
        ReservationModel.objects.filter(id=reservation_id).delete()