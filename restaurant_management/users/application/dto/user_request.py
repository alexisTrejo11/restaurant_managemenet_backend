from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class CreateUserRequestModel:
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
    role: str
    gender: str = "NOT_SPECIFIED"
    birth_date: Optional[datetime] = None
    phone_number: Optional[str] = None


@dataclass
class UpdateUserRequestModel:
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    birth_date: Optional[datetime] = None
    role: Optional[str] = None
    phone_number: Optional[str] = None