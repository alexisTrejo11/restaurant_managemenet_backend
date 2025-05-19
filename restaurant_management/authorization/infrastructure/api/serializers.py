from rest_framework import serializers
import re
from datetime import  date
from users.domain.valueobjects.gender import Gender
import datetime
from users.infrastructure.api.http.api.v1.serializers.serializers import EnumField 


class SignupValidator:
    @staticmethod
    def validate_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_phone(phone: str) -> bool:
        pattern = r'^\+?1?\d{9,15}$'
        return bool(re.match(pattern, phone))

    @staticmethod
    def validate_birth_date(birth_date: date) -> bool:
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return 18 <= age <= 100


class LoginSerializer(serializers.Serializer):
    identifier_field = serializers.CharField(
        error_messages={
            'required': 'identifeier_field is required',
            'invalid': 'Please enter a valid email address or phone number'
        }
    )
    password = serializers.CharField(
        error_messages={
            'required': 'Password is required'
        }
    )


class LoginResponseSerializer(serializers.Serializer):
    """Serializer for login response data"""
    access_token = serializers.CharField()
    token_type = serializers.CharField()
    expires_in = serializers.IntegerField()
    user = serializers.DictField()


class PasswordResetSerializer(serializers.Serializer):
    """Optional serializer for password reset"""
    email = serializers.EmailField(
        error_messages={
            'required': 'Email is required',
            'invalid': 'Please enter a valid email address'
        }
    )

    def validate_email(self, value: str) -> str:
        return value.lower()
    
class StaffSignupSerializer(serializers.Serializer):
    first_name = serializers.CharField(
        max_length=255,
        min_length=2,
        trim_whitespace=True,
        error_messages={
            'blank': 'El nombre no puede estar vacío',
            'max_length': 'El nombre no puede exceder los 255 caracteres',
            'min_length': 'El nombre debe tener al menos 2 caracteres'
        }
    )
    
    last_name = serializers.CharField(
        max_length=255,
        min_length=2,
        trim_whitespace=True,
        error_messages={
            'blank': 'El apellido no puede estar vacío',
            'max_length': 'El apellido no puede exceder los 255 caracteres',
            'min_length': 'El apellido debe tener al menos 2 caracteres'
        }
    )
    
    gender = EnumField(
        enum_type=Gender,
        error_messages={
            'invalid': 'Género no válido',
            'null': 'El género no puede ser nulo'
        }
    )
    
    email = serializers.EmailField(
        max_length=255,
        error_messages={
            'invalid': 'Por favor ingrese un correo electrónico válido',
            'blank': 'El correo electrónico no puede estar vacío'
        }
    )
    
    password = serializers.CharField(
        min_length=8,
        max_length=128,
        error_messages={
            'blank': 'La contraseña no puede estar vacía',
            'min_length': 'La contraseña debe tener al menos 8 caracteres',
            'max_length': 'La contraseña no puede exceder los 128 caracteres'
        }
    )
    
    birth_date = serializers.DateField(
        error_messages={
            'invalid': 'Formato de fecha inválido. Use YYYY-MM-DD',
            'blank': 'La fecha de nacimiento no puede estar vacía'
        }
    )
    
    phone_number = serializers.CharField(
        max_length=15,
        allow_null=True,
        required=False,
        allow_blank=True,
        error_messages={
            'max_length': 'El número telefónico no puede exceder los 15 caracteres'
        }
    )
    
    def validate_phone_number(self, value):
        if value and not value.isdigit():
            raise serializers.ValidationError("El número telefónico solo debe contener dígitos")
        return value
    
    def validate_birth_date(self, value):
        today = datetime.date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 18:
            raise serializers.ValidationError("Debe ser mayor de 18 años")
        return value