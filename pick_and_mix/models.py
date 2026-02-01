from django.db import models
from django.utils.text import slugify

from products.models import Product

# Create your models here.


class PickAndMixBag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    max_weight_in_grams = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    sweets = models.ManyToManyField(Product, blank=True, related_name='pick_and_mix_bag')

    def save(self, *args, **kwargs):
        """
        A function to automatically create a slug name
        for cleaner urls and database sorting
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
