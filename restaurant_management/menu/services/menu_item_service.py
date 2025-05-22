from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from ..models import MenuItemModel
from django.core.cache import cache


class MenuItemService:
    @staticmethod
    def validate_category(category: str) -> str:
        """Valida que la categoría exista en las opciones"""
        valid_categories = dict(MenuItemModel.CATEGORY_CHOICES).keys()
        if category not in valid_categories:
            raise ValidationError(f"Categoría inválida. Opciones válidas: {', '.join(valid_categories)}")
        return category

    @staticmethod
    def validate_price(price: Decimal) -> Decimal:
        """Valida reglas de negocio para precios"""
        if price <= Decimal('0.00'):
            raise ValidationError("El precio debe ser positivo")
        if price.as_tuple().exponent < -2:
            raise ValidationError("Máximo 2 decimales")
        if price > Decimal('10000.00'):
            return ValidationError("Precio no puede superar 10000.00")

    @staticmethod
    def create_menu_item(**kwargs) -> MenuItemModel:
        """Versión mejorada con más controles"""
        try:
            kwargs['name'] = kwargs['name'].strip().title()
            kwargs.setdefault('status', 'ACTIVE')
            return MenuItemModel.objects.create(**kwargs)
        except IntegrityError as e:
            raise ValidationError(str(e))

    @staticmethod
    def update_menu_item(instance: MenuItemModel, **kwargs) -> MenuItemModel:
        """Actualiza un ítem existente con validación de negocio"""
        if 'name' in kwargs:
            if MenuItemModel.objects.filter(
                name__iexact=kwargs['name']
            ).exclude(id=instance.id).exists():
                raise ValidationError("Ya existe otro ítem con este nombre")
            kwargs['name'] = kwargs['name'].strip().title()

        if 'description' in kwargs:
            kwargs['description'] = kwargs['description'].strip()

        for attr, value in kwargs.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
    
    @staticmethod
    def validate_status(status: str) -> str:
        valid_statuses = [choice[0] for choice in MenuItemModel.STATUS_CHOICES]
        if status not in valid_statuses:
            raise ValidationError(
                f"Invalid status parameter. Valid choices: {', '.join(valid_statuses)}"
            )
        return status
    
    @staticmethod
    def list_all_categories():
        cached = cache.get('menu_categories')
        if not cached:
            cached = [
                {"id": idx+1, "category": v} 
                for idx, (v, l) in enumerate(MenuItemModel.CATEGORY_CHOICES)
            ]
            cache.set('menu_categories', cached, timeout=86400)
        return cached