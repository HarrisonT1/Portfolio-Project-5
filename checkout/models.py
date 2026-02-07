import uuid
from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
from decimal import Decimal

from products.models import Product
from pick_and_mix.models import PickAndMixBag

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
    order_total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    order_fulfilled = models.BooleanField(default=False)

    def _generate_order_number(self):
        return uuid.uuid4().hex.upper()

    def update_total(self):
        self.order_total = self.lineitems.aggregate(
            models.Sum('line_item_total')
            )['line_item_total__sum'] or Decimal('0.00')

        if self.order_total >= settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = Decimal('0.00')
        else:
            if self.delivery_method == 'premium':
                self.delivery_cost = settings.PREMIUM_DELIVERY_COST
            else:
                self.delivery_cost = settings.STANDARD_DELIVERY_COST
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.order_number)


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    line_item_total = models.DecimalField(max_digits=6, decimal_places=2)
    pick_and_mix_bag = models.ForeignKey(PickAndMixBag, null=True, blank=True, on_delete=models.SET_NULL)
    pick_and_mix_item = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.product:
            return f'{self.product.name} x {self.quantity}'
        elif self.pick_and_mix_bag:
            return f'{self.pick_and_mix_bag.name} x {self.quantity}'
        return f'Product x {self.quantity}'

    def save(self, *args, **kwargs):
        if self.product:
            self.line_item_total = self.product.price * self.quantity
        elif self.pick_and_mix_bag:
            self.line_item_total = self.pick_and_mix_bag.price * self.quantity
        super().save(*args, **kwargs)
        self.order.update_total()
