from restaurant.services.domain.ingredient import Ingredient
from restaurant.services.domain.payment import Payment

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


    
class CompletePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['payment_method']

    tip = serializers.IntegerField(default=0)
    payment_method = serializers.CharField(required=True)

    def validate_payment_method(self, value):
        valid_payment_methods = dict(Payment.payment_method_choices).keys()
        if value not in valid_payment_methods:
            raise serializers.ValidationError("El método de pago proporcionado no es válido.")
        return value




"""

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