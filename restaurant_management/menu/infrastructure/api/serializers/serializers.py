from rest_framework import serializers


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