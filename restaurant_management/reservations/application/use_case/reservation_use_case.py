from ..service.reservation_service import ReservationService 
from datetime import datetime
from core.exceptions.custom_exceptions import EntityNotFoundException
from ..mappers.reservation_mapper import ReservationMapper
from ..dto.reservation_dto import ReservationDTO
from typing import List
from injector import inject


class RequestReservationUseCase:
    @inject
    def __init__(self, reservation_service: ReservationService):
        self.reservation_service = reservation_service

    def execute(self, reservation_data: dict) -> ReservationDTO:
        reservation_with_table = self.reservation_service.assign_table(reservation_data)
        
        reservation_created = self.reservation_service.create(reservation_with_table)   
        
        return ReservationMapper.to_dto(reservation_created)

class UpdateReservationUseCase:
    @inject
    def __init__(self, reservation_service: ReservationService):
        self.reservation_service = reservation_service

    def execute(self, reservation_data: dict, reservation_id: int):
        existing_reservation = self.reservation_service.get_by_id(reservation_id)
        if not existing_reservation:
            return EntityNotFoundException("Reservation", reservation_id)
        
        reservation_updated = self.reservation_service.update(reservation_data, existing_reservation)
        return ReservationMapper.to_dto(reservation_updated)

class CancelReservationUseCase:
    @inject
    def __init__(self, reservation_service: ReservationService):
        self.reservation_service = reservation_service

    def execute(self, reservation_id: int):
        reservation = self.reservation_service.get_by_id(reservation_id)
        if not reservation:
            return EntityNotFoundException("Reservation", reservation_id)
        
        self.reservation_service.cancel()    
    

class GetTodaysReservationUseCase:
    @inject
    def __init__(self, reservation_service: ReservationService) -> List[ReservationDTO]:
        self.reservation_service = reservation_service

    def execute(self):
        now = datetime.now()
        today_start_day = now.replace(hour=1, minute=0, second=0)
        today_end_day = now.replace(hour=23, minute=59, second=59) 

        reservations = self.reservation_service.get_by_time_range(today_start_day, today_end_day)
        
        return [ReservationMapper.to_dto(reservation) for reservation in reservations]


class GetReservationsByDateRangeUseCase:
    @inject
    def __init__(self, reservation_service: ReservationService):
        self.reservation_service = reservation_service

    def execute(self,start_date: datetime, end_date: datetime):
        reservations = self.reservation_service.get_by_time_range(start_date, end_date)
        return [ReservationMapper.to_dto(reservation) for reservation in reservations]

