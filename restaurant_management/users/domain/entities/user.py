from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
import re
from ..valueobjects.user_roles import UserRole
from ..valueobjects.gender import Gender
from ..exceptions.user_exceptions import *

@dataclass
class User:
    username: str
    email: str
    first_name: str
    last_name: str
    role: UserRole
    
    id: int = None
    gender: Gender = Gender.NOT_SPECIFIED
    password: Optional[str] = None
    birth_date: Optional[datetime] = None
    phone_number: Optional[str] = None
    joined_at: datetime = field(default_factory=datetime.now)
    last_login: Optional[datetime] = None
    is_active: bool = True
    def __post_init__(self):
        """Validates the initial values of the User object."""
        self.validate_email(self.email)
        if self.password is not None:
            self.validate_password(self.password)
        if self.phone_number is not None:
            self.validate_phone_number(self.phone_number)

    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def set_password(self, hashed_password: str) -> None:
        self.password = hashed_password

    def update_last_login(self) -> None:
        self.last_login = datetime.now()

    @staticmethod
    def validate_email(email: str) -> None:
        if not email:
            raise MissingEmailError("Email is required")

        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise InvalidEmailError("Invalid email format")

    @staticmethod
    def validate_password(password: str) -> None:
        if not password:
            raise MissingPasswordError("Password is required")

        if len(password) < 8:
            raise InvalidPasswordError("Password must be at least 8 characters long")

        if not any(c.isupper() for c in password):
            raise InvalidPasswordError("Password must contain at least one uppercase letter")

        if not any(c.islower() for c in password):
            raise InvalidPasswordError("Password must contain at least one lowercase letter")

        if not any(c.isdigit() for c in password):
            raise InvalidPasswordError("Password must contain at least one digit")

    @staticmethod
    def validate_phone_number(phone: Optional[str]) -> None:
        if not phone:
            return

        phone_pattern = r'^\+?[0-9]{10,15}$'
        if not re.match(phone_pattern, phone):
            raise InvalidPhoneNumberError("Invalid phone number format")