from shared.repository.common_repository import CommonRepository
from abc import ABC, abstractmethod
from typing import List
from ...core.domain.entities.order_entity import Order

class OrderRepository(CommonRepository[Order]):
    @abstractmethod
    def get_by_status(self, status: str) -> List[Order]:
        pass

    @abstractmethod
    def search(self, search_filters: dict) -> List[Order]:
        pass

    @abstractmethod
    def validate_not_conflict(self, order: Order) -> None:
        pass


