from django.forms import ValidationError
from users.models import User

#TODO: Implement Result Pattern
class AuthService:
    @staticmethod
    def validate_signup_data(email: str, password: str, password2: str) -> None:
        """Validates registration data before creating the user"""
        if User.objects.filter(email=email).exists():
            raise ValidationError("The email is already registered")
        
        if password != password2:
            raise ValidationError("Passwords do not match")

    @staticmethod
    def authenticate_user(email: str, password: str) -> User:
        try:
            user = User.objects.get(email=email)
            if user.check_password(password) and user.is_active:
                return user
            raise ValidationError("Invalid credentials")
        except User.DoesNotExist:
            raise ValidationError("User not found")