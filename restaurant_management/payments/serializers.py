from rest_framework import serializers

class PaymentItemSerializer(serializers.Serializer):
    menu_item_name = serializers.CharField(source='menu_item.name') 
    order_item_id = serializers.CharField(source='order_item.id') 
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField()
    total = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
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