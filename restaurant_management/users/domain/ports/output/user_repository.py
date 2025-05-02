from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from ...entities.user import User

class UserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: UUID) -> Optional[User]:
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def get_by_phone(self, phone_number: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[User]:
        pass
    
    @abstractmethod
    def save(self, user: User) -> User:
        pass
    
    @abstractmethod
    def delete(self,  user: User) -> bool:
        pass
    
    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        pass
    
    @abstractmethod
    def exists_by_phone(self, phone_number: str) -> bool:
        pass