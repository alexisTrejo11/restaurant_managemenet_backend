
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from ...domain.entities.reservation import Reservation
from orders.core.domain.entities.table_entity import Table

class ReservationRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Reservation]:
        """
        Obtiene todas las reservaciones.
        """
        pass

    @abstractmethod
    def get_by_id(self, reservation_id: int) -> Optional[Reservation]:
        """
        Obtiene una reservación por su ID.
        """
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> List[Reservation]:
        """
        Obtiene todas las reservaciones asociadas a un correo electrónico.
        """
        pass

    @abstractmethod
    def get_by_phone_number(self, phone_number: str) -> List[Reservation]:
        """
        Obtiene todas las reservaciones asociadas a un número de teléfono.
        """
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> List[Reservation]:
        """
        Obtiene todas las reservaciones asociadas a un nombre.
        """
        pass

    @abstractmethod
    def get_by_table(self, table_number: int) -> List[Reservation]:
        """
        Obtiene todas las reservaciones asociadas a una mesa específica.
        """
        pass

    @abstractmethod
    def get_reservations_by_date_range(self, start: datetime, end: datetime) -> List[Reservation]:
        """
        Obtiene todas las reservaciones dentro de un rango de fechas.
        """
        pass

    @abstractmethod
    def get_by_table_and_reservation_time(self, table_number: int, reservation_date: datetime) -> Optional[Reservation]:
        """
        Busca si ya existe una reservación para una mesa y fecha específicas.
        """
        pass

    @abstractmethod
    def save(self, reservation: Reservation) -> Reservation:
        """
        Guarda una nueva o actualiza una reservación existente.
        """
        pass

    @abstractmethod
    def delete(self, reservation_id: int) -> None:
        """
        Elimina una reservación por su ID.
        """
        pass