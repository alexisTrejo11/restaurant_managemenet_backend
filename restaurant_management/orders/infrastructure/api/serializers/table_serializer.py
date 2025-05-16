from rest_framework import serializers
from ...models.table_model import TableModel

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableModel
        fields = ['__all__']

