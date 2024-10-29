from restaurant.models import Table, Ingredient, Menu, Reservation, Stock
from rest_framework import serializers

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['number', 'is_available', 'seats']  
        read_only_fields = ['id']  


class IngredientInsertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity', 'unit']  
        read_only_fields = ['id']  


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
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

