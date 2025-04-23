from django.db import models

class TableModel(models.Model):
    number = models.IntegerField()
    capacity = models.IntegerField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

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
    created_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'orders'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f'Order {self.id} - Table {self.table.number}'


class OrderItemModel(models.Model):
    menu_item = models.ForeignKey('menu.MenuItemModel', on_delete=models.PROTECT, related_name='order_items')
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name='order_items', default="")
    added_at = models.DateTimeField(auto_now_add=True)
    menu_extra = models.ForeignKey('menu.MenuExtraModel', on_delete=models.PROTECT, related_name='order_items', null=True)
    quantity = models.IntegerField(default=1)
    notes = models.TextField(null=True, blank=True) 
    is_delivered = models.BooleanField(default=False)

    class Meta:
        db_table = 'order_items'
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f'{self.menu_item.name} - Order {self.order.id if self.order else "Unknown"}'

