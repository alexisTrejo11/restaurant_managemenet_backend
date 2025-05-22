from rest_framework import viewsets
from .models import Table
from .serializers import TableSerializer
from core.response.django_response import DjangoResponseWrapper as ResponseWrapper
from .services.table_service import TableService
import logging

logger = logging.getLogger(__name__)

class TableViews(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    lookup_field = 'number'
    lookup_url_kwarg = 'number'


    def list(self, request, *args, **kwargs):
        user_id = getattr(request.user, 'id', 'Anonymous') 
        logger.info(f"User {user_id} is requesting table list.")
        
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        logger.info(f"Returning {len(queryset)} tables.")
        return ResponseWrapper.found(
            data=serializer.data,
            entity="Table List",
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user_id = getattr(request.user, 'id', 'Anonymous')
        logger.info(f"User {user_id} is requesting details for table ID: {instance.id}.")
        
        serializer = self.get_serializer(instance)

        logger.info(f"Returning details for table ID: {instance.id}.")
        return ResponseWrapper.found(
            data=serializer.data,
            entity=f"Table {instance.id}",
        )

    def create(self, request, *args, **kwargs):
        user_id = getattr(request.user, 'id', 'Anonymous')
        logger.info(f"User {user_id} is attempting to create a new table with data: {request.data}.")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        created_table = TableService.create_table(serializer.validated_data)

        logger.info(f"Table ID: {created_table.id} created successfully by user {user_id}.")
        return ResponseWrapper.created(
            data=self.get_serializer(created_table).data,
            entity=f"Table {created_table.id}",
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        user_id = getattr(request.user, 'id', 'Anonymous')
        logger.info(f"User {user_id} is attempting to update table ID: {instance.id} with data: {request.data}.")

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        updated_table = TableService.update_table(instance, serializer.validated_data)

        logger.info(f"Table ID: {updated_table.id} updated successfully by user {user_id}.")
        return ResponseWrapper.updated(
            data=self.get_serializer(updated_table).data,
            entity=f"Table {updated_table.id}",
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user_id = getattr(request.user, 'id', 'Anonymous')
        logger.info(f"User {user_id} is attempting to delete table ID: {instance.id}.")

        table_id = instance.id 
        TableService.delete_table(instance)

        logger.info(f"Table ID: {table_id} deleted successfully by user {user_id}.")
        return ResponseWrapper.deleted(
            entity=f"Table {table_id}",
        )