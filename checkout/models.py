import uuid
from django.db import models
from django.conf import settings
from django_countries.fields import CountryField

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
            self.order_number = self._generate_order_number
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number
