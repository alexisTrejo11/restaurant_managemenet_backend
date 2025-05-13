from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, List, Any

from orders.application.dtos.table_dto import TableDTO

@dataclass
class ReservationDTO:
    name: str
    email: str
    phone_number: str
    customer_number: int
    reservation_date: datetime
    status: str = "BOOKED"
    table: Optional[TableDTO] = None
    created_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None
    id: Optional[int] = None

    def to_dict(self) -> dict:
        """
        Convierte el DTO a un diccionario con valores serializables.
        Las fechas se convierten a formato ISO (ej: '2025-04-05T12:30:00').
        """
        data = asdict(self)

        # Convertir campos datetime a string ISO
        for field in ['reservation_date', 'created_at', 'cancelled_at']:
            if isinstance(data.get(field), datetime):
                data[field] = data[field].isoformat()

        return data