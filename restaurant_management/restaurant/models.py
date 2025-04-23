from django.db import models
from django.utils import timezone
from django.utils.timezone import now
from decimal import Decimal

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
    table = models.ForeignKey('orders.TableModel', on_delete=models.PROTECT, related_name='reservations')
    reservation_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'reservations'
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'

    def __str__(self):
        return f'{self.name} - {self.reservation_date}'
