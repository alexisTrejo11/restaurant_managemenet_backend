import email
from restaurant.services.domain.table import Table
from restaurant.services.domain.ingredient import Ingredient
from restaurant.services.domain.menu_item import MenuItem
from datetime import datetime
from restaurant.services.domain import table

from rest_framework import serializers


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



"""
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class CompletePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['payment_method', 'tip']

    tip = serializers.IntegerField(default=0)
    payment_method = serializers.CharField(required=True)

    def validate_payment_method(self, value):
        valid_payment_methods = dict(Payment.payment_method_choices).keys()
        if value not in valid_payment_methods:
            raise serializers.ValidationError("El método de pago proporcionado no es válido.")
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['menu_item', 'quantity', 'notes']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)  

    class Meta:
        model = Order
        fields = ['id', 'table', 'created_at', 'status', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')  # Extract items data
        order = Order.objects.create(**validated_data)  # Create the Order

        # Create related OrderItems
        OrderItem.objects.bulk_create([
            OrderItem(order=order, **item_data) for item_data in items_data
        ])
        
        return order


class OrderItemInsertSerializer(serializers.Serializer):
    menu_id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(required=True, min_value=1)
    notes = serializers.CharField(required=False)


class AddItemsSerilizer(serializers.Serializer):
     order_items = serializers.ListField(
        child=OrderItemInsertSerializer(),  
        required=True,
        allow_empty=False
    )

class OrderInsertSerializer(serializers.Serializer):
    table_number = serializers.IntegerField(required=True, min_value=1)
    order_items = serializers.ListField(
        child=OrderItemInsertSerializer(),  
        required=True,
        allow_empty=False
    )

    def validate_order_items(self, value):
        if not value:
            raise serializers.ValidationError("Order items cannot be empty.")
        return value

class StockInsertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['optimal_quantity']  
        read_only_fields = ['id']


class StockUpdateSerializer(serializers.Serializer):
    ingredient_id = serializers.IntegerField()
    update_status = serializers.ChoiceField(choices=['IN', 'OUT'])
    quantity = serializers.IntegerField()

    def validate_quantity(self, value):
        Validate that the quantity is a positive number.
    
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive number.")
        return value

    def validate_update_status(self, value):
        Validate that the update status is 'IN' or 'OUT'.
        if value not in ['IN', 'OUT']:
            raise serializers.ValidationError("Update status must be 'IN' or 'OUT'.")
        return value

"""