from django.forms import CharField
from rest_framework import serializers
import re
from datetime import  date
from enum import Enum
from restaurant.services.domain.user import Gender, Role

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


class EnumField(serializers.ChoiceField):
    """Custom serializer field for Enum types."""
    def __init__(self, enum_type: Enum, **kwargs):
        self.enum_type = enum_type
        choices = [(e.value, e.name) for e in enum_type]
        super().__init__(choices=choices, **kwargs)

    def to_representation(self, obj):
        return obj.value

    def to_internal_value(self, data):
        try:
            return self.enum_type(data)
        except ValueError:
            self.fail("invalid_choice", input=data)

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    gender = CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True) 
    birth_date = serializers.DateTimeField()
    role = CharField()
    joined_at = serializers.DateTimeField()
    last_login = serializers.DateTimeField()
    phone_number = serializers.CharField(max_length=15, allow_null=True, required=False)


class UserInsertSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    gender = EnumField(enum_type=Gender)
    email = serializers.EmailField()
    password = serializers.CharField()
    birth_date = serializers.DateField()
    role = EnumField(enum_type=Role)
    phone_number = serializers.CharField(max_length=15, allow_null=True, required=False)
