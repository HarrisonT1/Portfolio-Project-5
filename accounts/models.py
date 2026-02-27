# Standard libary imports
# Third-party imports
from django_countries.fields import CountryField
# Django imports
from django.contrib.auth.models import User
from django.db import models
# Local imports

# Create your models here.


class UserAccount(models.Model):
    """
    Stores a user's default delivery and contact information
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    default_full_name = models.CharField(max_length=60, blank=True)
    default_email = models.CharField(max_length=60, blank=True)
    default_phone_number = models.CharField(max_length=60, blank=True)
    default_country = CountryField(
        max_length=60, blank=True, blank_label='Select a country')
    default_postcode = models.CharField(max_length=60, blank=True)
    default_city = models.CharField(max_length=60, blank=True)
    default_town = models.CharField(max_length=60, blank=True)
    default_street_address1 = models.CharField(max_length=60, blank=True)
    default_street_address2 = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return self.user.username
