import uuid
from django.db import models
from django.conf import settings
from django_countries.fields import CountryField

from products.models import Product

# Create your models here.


class Order(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    order_number = models.CharField(max_length=32, editable=False, unique=True)

    date_time = models.DateTimeField(auto_now_add=True)
    country = CountryField()
    postcode = models.CharField(max_length=15)
    city = models.CharField(max_length=80)
    town = models.CharField(max_length=80)
    street_address1 = models.CharField(max_length=80)
    street_address2 = models.CharField(max_length=80, blank=True)

    delivery_method = models.CharField(choices=settings.DELIVERY_OPTIONS)

    def _generate_order_number(self):
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.order_number)


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    line_item_total = models.DecimalField(max_digits=6, editable=False, decimal_places=2)

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'

    def save(self, *args, **kwargs):
        self.line_item_total = self.product.price * self.quantity
        super().save(*args, **kwargs)
