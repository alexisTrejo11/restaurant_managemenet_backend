from django.db import models
from django.utils import timezone

class IngredientModel(models.Model):
    menu_item = models.ForeignKey('menu.MenuItemModel', on_delete=models.SET_NULL, null=True, related_name='ingredients')
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

    class Meta:
        db_table = 'ingredients'
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return self.name
