from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):

    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('books', 'Books'),
        ('home', 'Home & Kitchen'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=30)
    description = models.TextField()
    category = models.CharField (max_length=20, choices=CATEGORY_CHOICES, default='other')
    stock = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=255)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.name

    def in_stock(self):
        return self.stock > 0

