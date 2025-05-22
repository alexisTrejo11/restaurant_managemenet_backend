import django_filters
from .models import MenuItem
from decimal import Decimal

class MenuItemFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(
        field_name='price', 
        lookup_expr='gte',
        help_text="Filtra por precio mínimo"
    )
    max_price = django_filters.NumberFilter(
        field_name='price', 
        lookup_expr='lte',
        help_text="Filtra por precio máximo"
    )
    category = django_filters.ChoiceFilter(
        choices=MenuItem.CATEGORY_CHOICES,
        lookup_expr='iexact'
    )
    status = django_filters.ChoiceFilter(
        choices=MenuItem.STATUS_CHOICES,
        help_text="Filtra por estado (ACTIVE/INACTIVE)"
    )

    class Meta:
        model = MenuItem
        fields = {
            'name': ['icontains'],
            'description': ['icontains']
        }