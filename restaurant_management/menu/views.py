from rest_framework import generics, permissions, filters
from rest_framework.exceptions import NotFound
from shared.response.django_response import DjangoResponseWrapper
import logging
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import MenuItem
from .serializers import MenuItemSerializer
from .services.menu_item_service import MenuItemService
from .filters import MenuItemFilter
from rest_framework.decorators import api_view

logger = logging.getLogger(__name__)

class MenuDishRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        logger.info(
            f"Retrieve request for menu item ID: {kwargs.get('id')}",
            extra={'user': request.user.id, 'request_data': request.data}
        )
        
        instance = self.get_item_or_404()
        serializer = self.get_serializer(instance)
        
        logger.info(
            f"Successfully retrieved menu dish ID: {instance.id}",
            extra={'category': instance.category}
        )
        
        return DjangoResponseWrapper.found(
            data=serializer.data,
            entity="Menu Dish",
        )

    def update(self, request, *args, **kwargs):
        logger.info(
            f"Update request for menu item ID: {kwargs.get('id')}",
            extra={
                'user': request.user.id,
                'request_data': request.data,
                'method': request.method
            }
        )
        try:
            instance = self.get_item_or_404()
            serializer = self.get_serializer(instance, data=request.data, partial=bool(kwargs.get('partial')))
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            
            logger.info(
                f"Successfully updated menu dish ID: {instance.id}",
                extra={'updated_fields': list(request.data.keys())}
            )
            
            return DjangoResponseWrapper.updated(
                data=serializer.data,
                entity="Menu dish",
            )
        except serializers.ValidationError as e:
            logger.warning(
                f"Validation error updating menu dish: {str(e)}",
                extra={'invalid_data': request.data}
            )
            return DjangoResponseWrapper.bad_request(message=e.detail)
        
    def destroy(self, request, *args, **kwargs):
        logger.warning(
            f"Delete request for menu dish ID: {kwargs.get('id')}",
            extra={'user': request.user.id}
        )
        try:
            instance = self.get_item_or_404()
            self.perform_destroy(instance)
            
            logger.info(f"Successfully deleted menu item ID: {kwargs.get('id')}")
            
            return DjangoResponseWrapper.deleted(entity="Menu Item")
        except NotFound:
            return DjangoResponseWrapper.not_found(
                message=f"Menu item with ID {kwargs.get('id')} not found"
            )
        
    def get_item_or_404(self):
        """Helper method with logging for object retrieval"""
        try:
            obj = super().get_object()
            logger.debug(f"Successfully retrieved menu item ID: {obj.id}")
            return obj
        except NotFound as e:
            logger.error(f"Menu item not found. Lookup params: {self.kwargs}")
            raise ValueError("Menu Item Not Found")



# TODO: Check Filters
class MenuDishCreateView(generics.ListCreateAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MenuItemFilter
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['name']  # Default

    def get_queryset(self):
        """Base queryset con filtro de status activo por defecto"""
        return MenuItem.objects.filter(status='ACTIVE')

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            
            # Paginación
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            query_params_dict = dict(request.query_params)

            logger.info(
                f"Listed {len(queryset)} menu items",
                extra={'filters': query_params_dict}
            )
            
            return DjangoResponseWrapper.success(
                data=serializer.data,
                metadata={
                    'total_items': queryset.count(),
                    'filters_applied': query_params_dict
                }
            )


        except Exception as e:
            logger.error(f"Error listing menu items: {str(e)}", exc_info=True)
            return DjangoResponseWrapper.internal_server_error(message="Error retrieving items")
    
    def create(self, request, *args, **kwargs):
        logger.info(
            "Create request for new menu item",
            extra={
                'user': request.user.id,
                'data': request.data
            }
        )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        menu_item = MenuItemService.create_menu_item(**serializer.validated_data)
        logger.info(
            f"Successfully created menu item ID: {menu_item.id}",
            extra={'item_id': menu_item.id}
        )
        
        return DjangoResponseWrapper.created(
            data=serializer.data, 
            entity="Menu Item"
        )

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ListActiveDishesByStatus(generics.ListAPIView):
    serializer_class = MenuItemSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']  

    def get_queryset(self):
        category = self.request.query_params.get('status', 'ACTIVE').upper()
        logger.info(
            f"Listing menu items with category: {category}",
            extra={
                'requested_by': self.request.user.id,
                'query_params': self.request.query_params
            }
        )
        MenuItemService.validate_category(category)
        return MenuItem.objects.filter(category=category, status="ACTIVE").order_by('name')

    def list(self, request, *args, **kwargs):        
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        return DjangoResponseWrapper.success(
                data=serializer.data,
                message=f"Menu items filtered by status",
                metadata={
                    'total_items': len(queryset),
                    'status_filter': self.request.query_params.get('status'),
                    'category_filter': self.request.query_params.get('category')
                }
        )
    

