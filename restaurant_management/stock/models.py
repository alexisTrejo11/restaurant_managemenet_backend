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


class StockModel(models.Model):
    ingredient = models.ForeignKey(IngredientModel, on_delete=models.PROTECT, related_name='stocks')
    total_stock = models.IntegerField()
    optimal_stock_quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

    def get_transactions(self):
        return self.transactions.all()

    class Meta:
        db_table = 'stocks'
        verbose_name = 'Stock'
        verbose_name_plural = 'Stocks'

    def __str__(self):
        return f'{self.ingredient.name} - {self.total_stock} {self.ingredient.unit}'


class StockTransactionModel(models.Model):
    TRANSACTION_TYPES = [
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
    ]

    ingredient_quantity = models.IntegerField()
    stock = models.ForeignKey(StockModel, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=3, choices=TRANSACTION_TYPES)
    date = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(null=True)
    employee_name = models.CharField(max_length=255, blank=True, null=True) 

    class Meta:
        db_table = 'stock_transactions'
        verbose_name = 'Stock Transaction'
        verbose_name_plural = 'Stock Transactions'

    def __str__(self):
        return f'{self.transaction_type} - {self.ingredient_quantity}'
