from django.db import models
from django.utils import timezone
from django.conf import settings
import pika
import json
from order_service.tasks import fetch_price


class Order(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('FULFILLED', 'fulfilled'),
        ('CANCELLED', 'Cancelled'),
    ]

    ordered_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order {self.id} - {self.ordered_by.username}"

    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderedItem(models.Model):

    STATUS_CHOICES = [
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('CANCELLED', 'Cancelled'),
        ('DELIVERED', 'Delivered'),
    ]

    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, default=None)
    product_id = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PROCESSING')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.product_name} - {self.order.id}"

    def get_cost(self):
        if self.price is None:
            self.fetch_price()
        return self.quantity * self.price

    def fetch_price(self):
        result = fetch_price.delay(self.product_id, self.id)
        self.price = result.get(timeout=10)
        self.save()
        return self.price
