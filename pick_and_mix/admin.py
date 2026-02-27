# Standard libary imports
# Third-party imports
# Django imports
from django.contrib import admin
# Local imports
from .models import PickAndMixBag

# Register your models here.


@admin.register(PickAndMixBag)
class PickAndMixBagAdmin(admin.ModelAdmin):
    """
    Registers pick and mix bags in the admin
    """
    list_display = ('name', 'price', 'max_weight_in_grams')
    filter_horizontal = ('sweets',)
