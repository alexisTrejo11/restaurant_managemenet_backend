from rest_framework import serializers

class StockTransactionInsertSerializer(serializers.Serializer):
    stock_id = serializers.IntegerField()
    transaction_type = serializers.CharField()
    ingredient_quantity = serializers.IntegerField()
    date = serializers.DateTimeField()
    employee_name = serializers.CharField()
    expires_at = serializers.DateTimeField(required=False, allow_null=True)

class StockInsertSerializer(serializers.Serializer):
    ingredient_id = serializers.IntegerField()
    optimal_stock_quantity = serializers.IntegerField()

class StockTransactionSerializer(serializers.Serializer):
    transaction_type = serializers.CharField()
    ingredient_quantity = serializers.IntegerField()
    date = serializers.DateTimeField()
    employee_name = serializers.CharField()
    expires_at = serializers.DateTimeField(required=False, allow_null=True)

class IngredientSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    unit = serializers.CharField()

class IngredientInsertSerializer(serializers.Serializer):
    name = serializers.CharField()
    unit = serializers.CharField()

class StockSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    total_stock = serializers.IntegerField()
    optimal_stock_quantity = serializers.IntegerField()
    stock_transactions = StockTransactionSerializer(many=True) 
    ingredient = IngredientSerializer()


