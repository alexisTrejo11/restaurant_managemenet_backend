from django.forms import ValidationError
from users.models import User
from django.contrib.auth import authenticate

class AuthService:
    @staticmethod
    def validate_signup_data(email: str, password: str, password2: str) -> None:
        """Valida los datos de registro antes de crear el usuario"""
        if User.objects.filter(email=email).exists():
            raise ValidationError("El email ya está registrado")
        
        if password != password2:
            raise ValidationError("Las contraseñas no coinciden")

    @staticmethod
    def authenticate_user(email: str, password: str) -> User:
        try:
            user = User.objects.get(email=email)
            if user.check_password(password) and user.is_active:
                return user
            raise ValidationError("Credenciales inválidas")
        except User.DoesNotExist:
            raise ValidationError("Usuario no encontrado")
