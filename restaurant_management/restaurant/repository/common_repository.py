from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional

T = TypeVar('T') 

class CommonRepository(Generic[T], ABC):
    @abstractmethod
    def create(self, entity: T) -> T:
        """Create an entity"""
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        """Get entity por ID"""
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        """Get all entities"""
        pass

    @abstractmethod
    def update(self, entity: T) -> T:
        """Update an entity"""
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        """Delete an entity"""
        pass