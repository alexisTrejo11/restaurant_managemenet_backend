from django.db import models

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

    order = models.OneToOneField('orders.OrderModel', on_delete=models.PROTECT, null=True, related_name='payment')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, null=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))  # Valor por defecto
    vat_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))  # Valor por defecto
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
        'menu.MenuItemModel', 
        on_delete=models.PROTECT, 
        related_name='payment_items'
    )
    menu_item_extra = models.ForeignKey(
        'menu.MenuExtraModel', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='payment_items'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    extras_charges = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))  # Valor por defecto
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'payment_items'
        verbose_name = 'Payment Item'
        verbose_name_plural = 'Payment Items'

    def __str__(self):
        return f'{self.quantity}x {self.menu_item.name} - {self.total}'
