from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

# Create your models here.


class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    default_full_name = models.CharField(max_length=60, blank=True)
    default_email = models.CharField(max_length=60, blank=True)
    default_phone_number = models.CharField(max_length=60, blank=True)
    default_country = CountryField(max_length=60, blank=True)
    default_postcode = models.CharField(max_length=60, blank=True)
    default_city = models.CharField(max_length=60, blank=True)
    default_town = models.CharField(max_length=60, blank=True)
    default_street_address1 = models.CharField(max_length=60, blank=True)
    default_street_address2 = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return self.user.username
