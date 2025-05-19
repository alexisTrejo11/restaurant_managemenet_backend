from django.forms import CharField
from rest_framework import serializers
from enum import Enum
from users.domain.valueobjects.gender import Gender
from users.domain.valueobjects.user_roles import UserRole


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
    role = EnumField(enum_type=UserRole)
    phone_number = serializers.CharField(max_length=15, allow_null=True, required=False)
