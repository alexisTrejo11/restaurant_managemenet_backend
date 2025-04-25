from restaurant.services.domain.ingredient import Ingredient
from rest_framework import serializers

class TableInsertSerializer(serializers.Serializer):
    number = serializers.IntegerField()
    capacity = serializers.IntegerField()

    def validate(self, attrs):
        return super().validate(attrs)


class IngredientInsertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity', 'unit']  
        read_only_fields = ['id']  

class ReservationInsertSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.CharField(required=False, allow_null=True)
    phone_number = serializers.CharField(required=False, allow_null=True, default="")
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



