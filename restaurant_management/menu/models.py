from django.db import models

class MenuItemModel(models.Model):
    CATEGORY_CHOICES = [
        ('DRINKS', 'Drinks'),
        ('ALCOHOL_DRINKS', 'Alcohol Drinks'),
        ('BREAKFASTS', 'Breakfasts'),
        ('STARTERS', 'Starters'),
        ('MEALS', 'Meals'),
        ('DESSERTS', 'Desserts'),
        ('EXTRAS', 'Extras'),
    ]

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

    class Meta:
        db_table = 'menu_items'
        verbose_name = 'Menu Item'
        verbose_name_plural = 'Menu Items'

    def __str__(self):
        return self.name


class MenuExtraModel(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

    class Meta:
        db_table = 'menu_extras'
        verbose_name = 'Menu Extra'
        verbose_name_plural = 'Menu Extras'

    def __str__(self):
        return self.name