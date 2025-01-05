from django.forms import CharField
from restaurant.services.domain.ingredient import Ingredient
from rest_framework import serializers
import re
from datetime import  date
from enum import Enum
from restaurant.services.domain.user import Gender, Role



class TableInsertSerializer(serializers.Serializer):
    number = serializers.IntegerField()
    capacity = serializers.IntegerField()


class TableSerializer(serializers.Serializer):
    number = serializers.IntegerField()
    capacity = serializers.IntegerField()
    is_available = serializers.BooleanField()


class IngredientInsertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity', 'unit']  
        read_only_fields = ['id']  


class IngredientSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    unit = serializers.CharField()

class IngredientInsertSerializer(serializers.Serializer):
    name = serializers.CharField()
    unit = serializers.CharField()

class MenuInsertItemSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    category = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def validate_category(self, value):
        """
        Validate that the category is one of the allowed values.
        """
        allowed_categories = [
            'DRINKS', 
            'ALCOHOL_DRINKS', 
            'BREAKFASTS', 
            'STARTERS', 
            'MEALS', 
            'DESSERTS', 
            'EXTRAS'
        ]
        if value not in allowed_categories:
            raise serializers.ValidationError(f"Invalid category '{value}'. Allowed categories are: {', '.join(allowed_categories)}.")
        return value


class MenuItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    category = serializers.CharField()
    description = serializers.CharField()


class StockInsertSerializer(serializers.Serializer):
    ingredient_id = serializers.IntegerField()
    optimal_stock_quantity = serializers.IntegerField()


class StockTransactionSerializer(serializers.Serializer):
    transaction_type = serializers.CharField()
    ingredient_quantity = serializers.IntegerField()
    date = serializers.DateTimeField()
    employee_name = serializers.CharField()
    expires_at = serializers.DateTimeField(required=False, allow_null=True)


class StockSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    total_stock = serializers.IntegerField()
    optimal_stock_quantity = serializers.IntegerField()
    stock_transactions = StockTransactionSerializer(many=True) 
    ingredient = IngredientSerializer()


class StockTransactionInsertSerializer(serializers.Serializer):
    stock_id = serializers.IntegerField()
    transaction_type = serializers.CharField()
    ingredient_quantity = serializers.IntegerField()
    date = serializers.DateTimeField()
    employee_name = serializers.CharField()
    expires_at = serializers.DateTimeField(required=False, allow_null=True)


class ReservationInsertSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.CharField(required=False, allow_null=True)
    phone_number = serializers.CharField(required=False, allow_null=True)
    reservation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    customer_number = serializers.IntegerField()


class ReservationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    email = serializers.CharField()
    phone_number = serializers.CharField()
    table = serializers.IntegerField(source='table.number')
    reservation_date = serializers.DateTimeField()  
    status = serializers.CharField()
    created_at = serializers.DateTimeField()

from rest_framework import serializers
from restaurant.repository.models.models import OrderModel, OrderItemModel

class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)  
    added_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")

    class Meta:
        model = OrderItemModel
        fields = ['id', 'menu_item_name', 'notes', 'quantity', 'is_delivered', 'added_at']


class OrderSerializer(serializers.ModelSerializer):
    table_number = serializers.IntegerField(source='table.number', read_only=True) 
    items = OrderItemSerializer(many=True, read_only=True, default=[])

    class Meta:
        model = OrderModel
        fields = ['id', 'table_number', 'status', 'created_at', 'end_at', 'items']


class OrderItemInsertSerializer(serializers.Serializer):
    menu_item_id = serializers.IntegerField()  
    quantity = serializers.IntegerField()
    notes = serializers.CharField(required=False)  
    menu_extra_id = serializers.IntegerField(required=False)  

    
class OrderItemsInsertSerilizer(serializers.Serializer):
    order_id = serializers.IntegerField()
    order_items = serializers.ListField(
        child=OrderItemInsertSerializer(),  
        required=True,
        allow_empty=False
    )

class OrderItemsDeleteSerilizer(serializers.Serializer):
    order_id = serializers.IntegerField()
    item_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True,
        allow_empty=False
    )


class OrderInitSerializer(serializers.ModelSerializer):
    table_number = serializers.IntegerField()
    order_items = serializers.ListField(
        child=OrderItemInsertSerializer(),  
        required=True,
        allow_empty=False
    )

    def validate_order_items(self, value):
        if not value:
            raise serializers.ValidationError("Order items cannot be empty.")
        return value


class PaymentItemSerializer(serializers.Serializer):
    menu_item_name = serializers.CharField(source='menu_item.name') 
    order_item_id = serializers.CharField(source='order_item.id') 
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField()
    total = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    #extra_item_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    menu_extra_item = serializers.CharField(required=False) 


class PaymentSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    order_id = serializers.IntegerField(source='order.id')
    payment_method = serializers.CharField(max_length=20)
    payment_status = serializers.CharField(max_length=20)
    sub_total = serializers.DecimalField(max_digits=10, decimal_places=2)
    discount = serializers.DecimalField(max_digits=10, decimal_places=2)
    vat_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    vat = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency_type = serializers.CharField(max_length=3)
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
    created_at = serializers.DateTimeField(required=False, allow_null=True, format='%Y-%m-%d %H:%M:%S')
    paid_at = serializers.DateTimeField(required=False, allow_null=True, format='%Y-%m-%d %H:%M:%S')
    items = serializers.ListField(
        child=PaymentItemSerializer(),  
        required=True,
        allow_empty=False
    )


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
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    gender = EnumField(enum_type=Gender)
    email = serializers.EmailField()
    password = serializers.CharField()
    birth_date = serializers.DateField()
    phone_number = serializers.CharField(max_length=15, allow_null=True, required=False)
    role = serializers.ChoiceField(choices=[(Role.STAFF, Role.STAFF.name)], default=Role.STAFF, read_only=True)
