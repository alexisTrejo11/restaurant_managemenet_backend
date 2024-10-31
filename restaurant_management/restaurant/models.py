from django.db import models
from datetime import datetime
from decimal import Decimal


class Table(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.PositiveIntegerField(unique=True)
    seats = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)

    def set_as_available(self):
        self.is_available = True

    def set_as_unavailable(self):
        self.is_available = False

    def __str__(self):
        return f"Table {self.number} (Seats: {self.seats})"
    

class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_available = models.BooleanField(default=True)

    CATEGORY_CHOICES = [
        ('undefined', 'Undefined'),
        ('drinks', 'Drinks'),
        ('alcohol_drinks', 'Alcohol Drinks'),
        ('starters', 'Starters'),
        ('breakfasts', 'Breakfasts'),
        ('meals', 'Meals'),
        ('desserts', 'Desserts'),
        ('extras', 'Extras'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='undefined', null=False)

    def __str__(self):
        return self.name


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status_choices = [
        ('in_progress', 'In progress'),  
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=15, choices=status_choices, default='pending')

    def __str__(self):
        return f"Order #{self.id} for Table {self.table.number}"
    
    @classmethod
    def validate_status(cls, status):
        return status in dict(cls.status_choices)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    notes = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} for Order #{self.order.id}"

    def get_menu_item(self):
        return self.menu_item


class Reservation(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField(null=True)
    customers_numbers = models.IntegerField(default=1)
    reservation_time = models.DateTimeField()

    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation for {self.customer_name} at {self.reservation_time}"


class Payment(models.Model):
    payment_method_choices = [
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
        ('digital_payment', 'Digital Payment'),
    ]
    
    status_choices = [
        ('pending_payment', 'Pending Payment'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    MEX_VAT = Decimal('0.16')

    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20, choices=payment_method_choices, default='cash')
    tip = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    VAT = models.DecimalField(max_digits=4, decimal_places=2, default=0.16)  
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=15, choices=status_choices, default='pending_payment')

    def __str__(self):
        return f"Payment of ${self.sub_total} for Order #{self.order.id}"


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20)  # kg, liters, etc.
    
    def __str__(self):
        return self.name


class Stock(models.Model):
    ingredient = models.OneToOneField(Ingredient, on_delete=models.CASCADE, related_name='stock')
    current_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    optimal_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Stock of {self.ingredient.name}"
    
    def is_below_optimal(self):
        return self.current_quantity < self.optimal_quantity  
    
    def increase_current_quantity(self, quantity):
        self.current_quantity += quantity

    def decrease_current_quantity(self, quantity):
        if self.current_quantity - quantity < 0:
            raise ValueError("Cannot decrease stock below zero")
        self.current_quantity -= quantity


class StockTransaction(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="transactions")
    date = models.DateTimeField(auto_now_add=True)
    stock_update_choices = [
        ('IN', 'in'),
        ('OUT', 'out'),
        ('ADJUSTED', 'adjusted'),
    ]
    stock_update = models.CharField(choices=stock_update_choices, max_length=20)
