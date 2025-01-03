from datetime import datetime
from enum import Enum
from dataclasses import dataclass
from typing import Optional
import re
from django.contrib.auth.hashers import make_password
from restaurant.utils.result import Result
from restaurant.utils.password_validator import PasswordValidator


class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class Role(Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"
    STAFF = "staff"

class UserException(Exception):
    """Base exception for User domain"""
    pass

class InvalidEmailException(UserException):
    """Raised when email format is invalid"""
    pass

class InvalidPhoneNumberException(UserException):
    """Raised when phone number format is invalid"""
    pass

@dataclass
class UserId:
    """Value object for User ID"""
    value: str

class User:
    def __init__(
        self, 
        first_name: str,
        last_name: str,
        gender: Gender,
        email: str,
        hashed_password: str,
        birth_date: datetime,
        role: Role,
        joined_at: datetime,
        last_login: datetime,
        phone_number: Optional[str] = None,
        id: Optional[UserId] = None,
    ):
        self.__id = id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__gender = gender
        self.__email = email
        self.__hashed_password = hashed_password
        self.__birth_date = birth_date
        self.__role = role
        self.__joined_at = joined_at
        self.__last_login = last_login
        self.__phone_number = phone_number if phone_number else None

    @property
    def id(self) -> Optional[UserId]:
        return self.__id

    @property
    def first_name(self) -> str:
        return self.__first_name

    @property
    def last_name(self) -> str:
        return self.__last_name

    @property
    def full_name(self) -> str:
        return f"{self.__first_name} {self.__last_name}"

    @property
    def gender(self) -> Gender:
        return self.__gender

    @property
    def email(self) -> str:
        return self.__email

    @property
    def birth_date(self) -> datetime:
        return self.__birth_date

    @property
    def role(self) -> Role:
        return self.__role

    @property
    def joined_at(self) -> datetime:
        return self.__joined_at

    @property
    def last_login(self) -> datetime:
        return self.__last_login

    @property
    def phone_number(self) -> Optional[str]:
        return self.__phone_number

    @property
    def hashed_password(self) -> str:
        return self.__hashed_password


    def hash_password(self, plain_password):
        hashed_password = make_password(plain_password)
        self.__hashed_password = hashed_password


    @staticmethod
    def validate_password(plain_password: str) -> Result:
        return PasswordValidator.validate_password_strict(plain_password)


    @staticmethod
    def validate_email(email: str) -> Result:
        email_pattern = re.compile(r'^[a-zA-Z0-9.__%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not email_pattern.match(email):
            return Result.error("Invalid email format")
        
        return Result.success()

    @staticmethod
    def validate_phone_number(phone_number: str) -> Result:
        phone_pattern = re.compile(r'^\+?1?\d{9,15}$')
        if not phone_pattern.match(phone_number):
            return Result.error("Invalid phone number format")
        
        return Result.success()
        

    def update_last_login(self, new_login_time: datetime) -> None:
        """Update the last login time"""
        self.__last_login = new_login_time


    def change_role(self, new_role: Role) -> None:
        """Change user's role"""
        self.__role = new_role


    def to_dict(self) -> dict:
        """Convert user to dictionary representation"""
        return {
            'id': str(self.__id.value) if self.__id else None,
            'first_name': self.__first_name,
            'last_name': self.__last_name,
            'gender': self.__gender.value,
            'email': self.__email,
            'birth_date': self.__birth_date.isoformat(),
            'role': self.__role.value,
            'joined_at': self.__joined_at.isoformat(),
            'last_login': self.__last_login.isoformat(),
            'phone_number': self.__phone_number
        }


    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return False
        return self.__id == other.__id


    def __hash__(self) -> int:
        return hash(self.__id)
    