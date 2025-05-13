from django.db import models

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
