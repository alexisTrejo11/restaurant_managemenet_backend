from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional

T = TypeVar('T') 

class CommonRepository(Generic[T], ABC):
    @abstractmethod
    def save(self, entity: T) -> Optional[T]:
        """Save an entity"""
        pass

    @abstractmethod
    def get_by_id(self, id: int, raise_expection=False) -> Optional[T]:
        """Get entity por ID, Raise an expection if set as True or will return a None"""
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        """Get all entities"""
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        """Delete an entity"""
        pass