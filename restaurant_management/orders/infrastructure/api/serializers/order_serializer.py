from rest_framework import serializers
from ...models.order_item_model import OrderItemModel
from ...models.order_model import OrderModel

class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)  
    menu_extra_name = serializers.CharField(source='menu_extra.name', read_only=True)  
    added_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")

    class Meta:
        model = OrderItemModel
        fields = ['id', 'menu_item_name', 'menu_extra_name','notes', 'quantity', 'is_delivered', 'added_at']


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

