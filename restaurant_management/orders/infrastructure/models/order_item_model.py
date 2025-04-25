from django.db import models
from .order_model import OrderModel

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

