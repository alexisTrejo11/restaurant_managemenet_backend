from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend

import logging

from ..models import Dish
from ..serializers import DishSerializer
from ..services.menu_item_service import DishService

from shared.response.django_response import DjangoResponseWrapper
from shared.pagination import CustomPagination

logger = logging.getLogger(__name__)

class ListActiveDishesByStatus(generics.ListAPIView):
    serializer_class = DishSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']  
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        category = self.request.query_params.get('status', 'ACTIVE').upper()
        logger.info(
            f"Listing menu items with category: {category}",
            extra={
                'requested_by': self.request.user.id,
                'query_params': self.request.query_params
            }
        )
        DishService.validate_category(category)
        return Dish.objects.filter(category=category, status="ACTIVE").order_by('name')

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
    
@api_view(['GET'])
def list_dish_status(request):
    status_list = DishService.list_all_categories()

    return DjangoResponseWrapper.found(
        data=status_list,
        entity="Dish Status List",
    )