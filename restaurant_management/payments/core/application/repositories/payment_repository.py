from core.repository.common_repository import CommonRepository
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional
from ...domain.entities.payment import Payment
from datetime import datetime


#TODO: Check
class PaymentRepository(CommonRepository(Payment, ABC)):
    @abstractmethod
    def get_by_order_id(self, order_id: int) -> Optional[Payment]:
        pass

    @abstractmethod
    def list_by_status(self, payment_status: str) -> List[Payment]:
        pass

    def list_by_date_range(self, start_date: datetime, end_date: datetime, only_completed=False) -> List[Payment]:
        pass