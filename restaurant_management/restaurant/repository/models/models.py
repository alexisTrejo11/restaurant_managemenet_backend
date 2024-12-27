from django.db import models
from django.utils import timezone
from django.utils.timezone import now


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
        

class MenuExtra(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'menu_extras'
        verbose_name = 'Menu Extra'
        verbose_name_plural = 'Menu Extras'

    def __str__(self):
        return self.name

class TableModel(models.Model):
    number = models.IntegerField()
    seats = models.IntegerField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tables'
        verbose_name = 'Table'
        verbose_name_plural = 'Tables'
        unique_together = ('number',)

    def __str__(self):
        return f'Table {self.number} ({self.seats} seats)'


class OrderModel(models.Model):
    STATUS_CHOICES = [
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    table = models.ForeignKey(TableModel, on_delete=models.PROTECT, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'orders'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f'Order {self.id} - Table {self.table.number}'


class OrderItem(models.Model):
    menu_item = models.ForeignKey(MenuItemModel, on_delete=models.PROTECT, related_name='order_items')
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name='order_items')
    added_at = models.DateTimeField(auto_now_add=True)
    is_delivered = models.BooleanField(default=False)

    class Meta:
        db_table = 'order_items'
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f'{self.menu_item.name} - Order {self.order.id}'


class IngredientModel(models.Model):
    menu_item = models.ForeignKey(MenuItemModel, on_delete=models.SET_NULL, null=True, related_name='ingredients')
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


class ReservationModel(models.Model):
    STATUS_CHOICES = [
        ('BOOKED', 'Booked'),
        ('ATTENDED', 'Attended'),
        ('NOT_ATTENDED', 'Not Attended'),
        ('CANCELLED', 'Cancelled'),
    ]

    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    customer_number = models.IntegerField()
    email = models.CharField(max_length=255)
    table = models.ForeignKey(TableModel, on_delete=models.PROTECT, related_name='reservations')
    reservation_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'reservations'
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.reservation_date}'


class PaymentModel(models.Model):
    PAYMENT_METHODS = [
        ('CASH', 'Cash'),
        ('CARD', 'Card'),
        ('TRANSACTION', 'Transaction'),
    ]

    PAYMENT_STATUS = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    CURRENCY_TYPES = [
        ('MXN', 'Mexican Peso'),
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
    ]

    order = models.OneToOneField(OrderModel, on_delete=models.PROTECT, null=True, related_name='payment')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    vat_rate = models.DecimalField(max_digits=5, decimal_places=2)
    vat = models.DecimalField(max_digits=10, decimal_places=2)
    currency_type = models.CharField(max_length=3, choices=CURRENCY_TYPES)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'payments'
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self):
        return f'Payment for Order {self.order_id} - {self.total} {self.currency_type}'