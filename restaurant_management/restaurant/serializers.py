from restaurant.models import Table, Ingredient
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
