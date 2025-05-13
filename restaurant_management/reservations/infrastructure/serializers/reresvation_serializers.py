from rest_framework import serializers
from rest_framework import serializers
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator

class ReservationInsertSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=100,
        min_length=2,
        error_messages={
            'max_length': 'The name cannot exceed 100 characters',
            'min_length': 'The name must be at least 2 characters long',
            'blank': 'The name is required'
        }
    )

    email = serializers.EmailField(
        required=False,
        allow_null=True,
        max_length=255,
        error_messages={
            'invalid': 'Enter a valid email address',
            'max_length': 'The email cannot exceed 255 characters'
        }
    )

    phone_number = serializers.CharField(
        required=False,
        allow_null=True,
        default="",
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^[0-9+()\- ]+$',
                message='The phone number can only contain digits and special characters (+ - () space)'
            )
        ],
        error_messages={
            'max_length': 'The phone number cannot exceed 20 characters'
        }
    )

    reservation_date = serializers.DateTimeField(
        format="%Y-%m-%dT%H:%M:%S",
        error_messages={
            'invalid': 'Invalid date format. Use YYYY-MM-DDTHH:MM:SS',
            'blank': 'The reservation date is required'
        }
    )

    customer_number = serializers.IntegerField(
        min_value=1,
        max_value=100,
        error_messages={
            'min_value': 'The number of customers must be at least 1',
            'max_value': 'The number of customers cannot exceed 100',
            'invalid': 'It must be a valid integer number',
            'blank': 'The number of customers is required'
        }
    )


class ReservationUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=100,
        min_length=2,
        error_messages={
            'max_length': 'The name cannot exceed 100 characters',
            'min_length': 'The name must be at least 2 characters long',
            'blank': 'The name is required'
        }
    )

    email = serializers.EmailField(
        required=False,
        allow_null=True,
        max_length=255,
        error_messages={
            'invalid': 'Enter a valid email address',
            'max_length': 'The email cannot exceed 255 characters'
        }
    )

    phone_number = serializers.CharField(
        required=False,
        allow_null=True,
        default="",
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^[0-9+()\- ]+$',
                message='The phone number can only contain digits and special characters (+ - () space)'
            )
        ],
        error_messages={
            'max_length': 'The phone number cannot exceed 20 characters'
        }
    )

    customer_number = serializers.IntegerField(
        min_value=1,
        max_value=100,
        error_messages={
            'min_value': 'The number of customers must be at least 1',
            'max_value': 'The number of customers cannot exceed 100',
            'invalid': 'It must be a valid integer number',
            'blank': 'The number of customers is required'
        }
    )


class ReservationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    email = serializers.CharField()
    phone_number = serializers.CharField()
    table = serializers.IntegerField(source='table.number')
    reservation_date = serializers.DateTimeField()  
    status = serializers.CharField()
    created_at = serializers.DateTimeField()


