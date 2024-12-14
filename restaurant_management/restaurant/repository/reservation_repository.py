from restaurant.services.domain.reservation import Reservation
from restaurant.repository.models.models import ReservationModel
from restaurant.mappers.reservation_mappers import ReservationMapper
from restaurant.repository.common_repository import CommonRepository
from typing import List, Optional


class ReservationRepository(CommonRepository):
    def __init__(self):
        self.reservation_model = ReservationModel

    def get_by_id(self, id: int) -> Optional[Reservation]:
        reservation = self.reservation_model.objects.filter(id=id).first()
        return ReservationMapper.to_domain(reservation) if reservation else None

    def get_by_table_and_reservation_time(self, table, reservation_date) -> Optional[Reservation]:
        start_time = reservation_date - timedelta(hours=2)
        end_time = reservation_date + timedelta(hours=2)
    
        reservation = self.reservation_model.objects.filter(
            table=table,
            reservation_date__range=(start_time, end_time)
        ).first()
        
        return ReservationMapper.to_domain(reservation) if reservation else None

    def get_by_email(self, email: str) -> List[Reservation]:
        return self._filter_by_field("email", email)


    def get_by_phone_number(self, phone_number: str) -> List[Reservation]:
        return self._filter_by_field("phone_number", phone_number)


    def get_reservations_by_date_range(self, start_date, end_date):
        reservations = self.reservation_model.objects.filter(reservation_date__range=(start_date, end_date))
        return [ReservationMapper.to_domain(r) for r in reservations] if reservations else []


    def create(self, new_reservation: Reservation) -> Reservation:
        reservation_model = ReservationMapper.to_model(new_reservation)
        reservation_model.save()
        return ReservationMapper.to_domain(reservation_model)


    def update(self, reservation: Reservation) -> Reservation:
        pass


    def get_all(self) -> List[Reservation]:
        reservation_models = self.reservation_model.objects.all()
        return [ReservationMapper.to_domain(model) for model in reservation_models] if reservation_models else []


    def delete(self, id: int) -> bool:
        deleted, _ = self.reservation_model.objects.filter(id=id).delete()
        return deleted > 0

    def _filter_by_field(self, field: str, value) -> List[Reservation]:
        reservations = self.reservation_model.objects.filter(**{field: value})
        return [ReservationMapper.to_domain(r) for r in reservations] if reservations else []

