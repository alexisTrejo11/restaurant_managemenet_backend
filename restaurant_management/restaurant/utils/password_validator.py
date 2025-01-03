from typing import Tuple
import re
from restaurant.utils.exceptions import PasswordValidationException
from restaurant.utils.result import Result

class PasswordValidator:
    MIN_LENGTH = 8
    MAX_LENGTH = 128
    SPECIAL_CHARS = "!@#$%^&*(),.?\":{}|<>-_+=`~'\\[]"
    
    @staticmethod
    def validate_password(plain_password: str) -> Tuple[bool, list[str]]:
        """
        Validates a password against security criteria.
        Returns a tuple of (is_valid: bool, error_messages: list[str])
        """
        errors = []

        # Check length
        if len(plain_password) < PasswordValidator.MIN_LENGTH:
            errors.append(f"Password must be at least {PasswordValidator.MIN_LENGTH} characters long")
        if len(plain_password) > PasswordValidator.MAX_LENGTH:
            errors.append(f"Password cannot exceed {PasswordValidator.MAX_LENGTH} characters")

        # Check for uppercase
        if not any(c.isupper() for c in plain_password):
            errors.append("Password must contain at least one uppercase letter")

        # Check for lowercase
        if not any(c.islower() for c in plain_password):
            errors.append("Password must contain at least one lowercase letter")

        # Check for numbers
        if not any(c.isdigit() for c in plain_password):
            errors.append("Password must contain at least one number")

        # Check for special characters
        if not any(c in PasswordValidator.SPECIAL_CHARS for c in plain_password):
            errors.append("Password must contain at least one special character")

        # Check for common patterns
        if re.search(r'(.)\1{2,}', plain_password):
            errors.append("Password cannot contain repeated characters (e.g., 'aaa')")

        # Check for sequential characters
        if any(str(plain_password[i:i+3]).lower() in 'abcdefghijklmnopqrstuvwxyz' for i in range(len(plain_password)-2)):
            errors.append("Password cannot contain sequential letters (e.g., 'abc')")
        
        if any(str(plain_password[i:i+3]) in '0123456789' for i in range(len(plain_password)-2)):
            errors.append("Password cannot contain sequential numbers (e.g., '123')")

        # Check for keyboard patterns
        keyboard_patterns = ['qwerty', 'asdfgh', 'zxcvbn']
        if any(pattern in plain_password.lower() for pattern in keyboard_patterns):
            errors.append("Password cannot contain keyboard patterns (e.g., 'qwerty')")

        return (len(errors) == 0, errors)

    @staticmethod
    def validate_password_strict(plain_password: str) -> Result:
        """
        Validates password and raises exception if invalid.
        Returns the password if valid.
        """
        is_valid, errors = PasswordValidator.validate_password(plain_password)
        if not is_valid:
            return Result.error("\n".join(errors))

        return Result.success()