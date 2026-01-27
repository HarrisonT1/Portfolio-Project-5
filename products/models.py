from django.db import models
from django.utils.text import slugify

# Create your models here.


class SweetCategory(models.Model):

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class DietaryTag(models.Model):

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    sweet_category = models.ForeignKey(
        SweetCategory,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='products')
    dietary_tag = models.ManyToManyField(
        DietaryTag,
        blank=True,
        related_name='products')
    sku = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(null=True, blank=True)
    in_stock = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        """
        A function to automatically create a slug name
        for cleaner urls and database sorting
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
