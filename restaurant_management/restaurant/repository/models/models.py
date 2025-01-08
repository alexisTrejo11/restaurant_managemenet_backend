from django.db import models
from django.utils import timezone
from django.utils.timezone import now
from decimal import Decimal
from django.contrib.auth.models import AbstractUser

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
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)

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
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)

    class Meta:
        db_table = 'menu_extras'
        verbose_name = 'Menu Extra'
        verbose_name_plural = 'Menu Extras'

    def __str__(self):
        return self.name


class TableModel(models.Model):
    number = models.IntegerField()
    capacity = models.IntegerField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)

    class Meta:
        db_table = 'tables'
        verbose_name = 'Table'
        verbose_name_plural = 'Tables'
        unique_together = ('number',)

    def __str__(self):
        return f'Table {self.number} ({self.capacity} capacity)'


class OrderModel(models.Model):
    STATUS_CHOICES = [
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    table = models.ForeignKey(TableModel, on_delete=models.PROTECT, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(default=now)
    end_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'orders'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f'Order {self.id} - Table {self.table.number}'


class OrderItemModel(models.Model):
    menu_item = models.ForeignKey(MenuItemModel, on_delete=models.PROTECT, related_name='order_items')
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name='order_items', default="")
    added_at = models.DateTimeField(default=now)
    menu_extra = models.ForeignKey(MenuExtraModel, on_delete=models.PROTECT, related_name='order_items', null=True)
    quantity = models.IntegerField(default=1)
    notes = models.CharField(null=True)
    is_delivered = models.BooleanField(default=False)

    class Meta:
        db_table = 'order_items'
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f'{self.menu_item.name} - Order {self.order.id if self.order else "Unknown"}'


class IngredientModel(models.Model):
    menu_item = models.ForeignKey(MenuItemModel, on_delete=models.SET_NULL, null=True, related_name='ingredients')
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=10)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)

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
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)

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
    created_at = models.DateTimeField(default=now)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'reservations'
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'

    def __str__(self):
        return f'{self.name} - {self.reservation_date}'


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
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, null=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    disccount = models.DecimalField(max_digits=10, decimal_places=2)
    vat_rate = models.DecimalField(max_digits=5, decimal_places=2)
    vat = models.DecimalField(max_digits=10, decimal_places=2)
    currency_type = models.CharField(max_length=3, choices=CURRENCY_TYPES)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=now)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'payments'
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self):
        return f'Payment for Order {self.order_id} - {self.total} {self.currency_type}'
    

class PaymentItemModel(models.Model):
    payment = models.ForeignKey(
        'PaymentModel', 
        on_delete=models.CASCADE, 
        related_name='payment_items'
    )
    order_item = models.OneToOneField(
        'OrderItemModel', 
        on_delete=models.PROTECT, 
        related_name='payment_item'
    )
    menu_item = models.ForeignKey(
        'MenuItemModel', 
        on_delete=models.PROTECT, 
        related_name='payment_items'
    )
    menu_item_extra = models.ForeignKey(
        'MenuExtra', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='payment_items'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'payment_items'
        verbose_name = 'Payment Item'
        verbose_name_plural = 'Payment Items'

    def __str__(self):
        return f'{self.quantity}x {self.menu_item.name} - {self.total}'

    def calculate_total(self):
        """Calculate the total price for the item."""
        return Decimal(self.price) * Decimal(self.quantity)
    

class UserModel(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateTimeField()
    role = models.CharField(max_length=20)
    joined_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    groups = models.ManyToManyField(
        'auth.Group', related_name='restaurant_usermodel_set', blank=True)
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='restaurant_usermodel_set', blank=True)

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"