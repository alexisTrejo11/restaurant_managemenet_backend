from .models import User
import re
from typing import Optional

class UserService:
    @staticmethod
    def validate_user_creation(user_data: dict):
        UserService.validate_email(user_data.get('email'))
        UserService.validate_password(user_data.get('password'))
        UserService.validate_phone_number(user_data.get('phone'))

    @staticmethod
    def validate_user_update(user_data: dict, current_user) -> None:
        """Validate business rules for user updates."""
        try:
            if 'email' in user_data:
                UserService.validate_email(user_data['email'])

            if 'password' in user_data:
                UserService.validate_password(user_data['password'])

            if 'phone_number' in user_data:
                UserService.validate_phone_number(user_data['phone_number'])

            if 'role' in user_data and user_data['role'] == 'admin':
                if not current_user.is_superuser:
                    raise UserUpdateError("Only admins can assign admin roles.")

        except (InvalidEmailError, InvalidPasswordError, InvalidPhoneNumberError) as e:
            raise UserUpdateError(str(e))


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
        

class UserError(Exception):
    """Base class for user-related exceptions."""
    pass

class InvalidEmailError(UserError):
    """Raised when the email format is invalid."""
    pass

class MissingEmailError(UserError):
    """Raised when the email is required but missing."""
    pass

class InvalidPasswordError(UserError):
    """Raised when the password does not meet complexity requirements."""
    pass

class MissingPasswordError(UserError):
    """Raised when the password is required but missing."""
    pass

class InvalidPhoneNumberError(UserError):
    """Raised when the phone number format is invalid."""
    pass

class UserUpdateError(Exception):
    """Raised when user update validation fails."""
    pass