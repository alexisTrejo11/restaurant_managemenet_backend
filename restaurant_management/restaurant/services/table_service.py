from restaurant.models import Table 
from restaurant.serializers import TableSerializer
from rest_framework.exceptions import ValidationError

class TableService:
    @staticmethod
    def get_table_by_number(number):
        try:
            table = Table.objects.get(number=number)
            serializer = TableSerializer(table)

            return serializer.data
        except Table.DoesNotExist:
            return None
    

    @staticmethod
    def get_tables_sorted_by_number():
        tables = Table.objects.all().order_by('number')  
        serializer = TableSerializer(tables, many=True) 
        return serializer.data
    

    @staticmethod
    def create_table(data):
        serializer = TableSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            raise ValidationError(serializer.errors) 


    @staticmethod
    def delete_table_by_number(number):
        try:
            table = Table.objects.get(number=number)
            table.delete()
            return True
        except Table.DoesNotExist:
            return False
