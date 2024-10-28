from restaurant.models import Table, Ingredient, Menu, Reservation, Stock
from rest_framework import serializers

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['number', 'is_available', 'seats']  
        read_only_fields = ['id']  


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity', 'unit']  
        read_only_fields = ['id']  


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
        fields = ['current_quantity', 'current_quantity']  
        read_only_fields = ['id']


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

