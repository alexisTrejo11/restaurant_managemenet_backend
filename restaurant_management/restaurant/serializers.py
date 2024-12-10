from restaurant.models import Table, Ingredient, MenuItem, Reservation, Stock, Order, OrderItem, Payment
from rest_framework import serializers

class TableInsertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['number', 'seats']  
        read_only_fields = ['id']  


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['number', 'seats', 'is_available'] 
        read_only_fields = ['id']  


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


class IngredientInsertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity', 'unit']  
        read_only_fields = ['id']  


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

        
class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['name', 'price', 'category', 'description']  
        read_only_fields = ['id']  


class ReservationInsertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['customer_name', 'customer_email', 'customers_numbers', 'reservation_time']  
        read_only_fields = ['id']


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'


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
        """
        Validate that the quantity is a positive number.
        """
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive number.")
        return value

    def validate_update_status(self, value):
        """
        Validate that the update status is 'IN' or 'OUT'.
        """
        if value not in ['IN', 'OUT']:
            raise serializers.ValidationError("Update status must be 'IN' or 'OUT'.")
        return value


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

