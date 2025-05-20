from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional
from uuid import UUID
import logging

from ...domain.entities.user import User

logger = logging.getLogger(__name__)

@dataclass
class UserResponse:
    id: str
    username: str
    email: str
    first_name: str
    last_name: str
    role: str
    gender: str
    birth_date: Optional[datetime] = None
    phone_number: Optional[str] = None
    joined_at: datetime = None
    last_login: Optional[datetime] = None
    is_active: bool = True

    @classmethod
    def from_entity(cls, user: User):
        return cls(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role,
            gender=user.gender,
            birth_date=user.birth_date,
            phone_number=user.phone_number,
            joined_at=user.joined_at,
            last_login=user.last_login,
            is_active=user.is_active
        )

    def to_dict(self) -> dict:
        """Converts the UserResponse object to a dictionary."""
        return asdict(self)