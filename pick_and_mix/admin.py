from django.contrib import admin
from .models import PickAndMixBag

# Register your models here.


@admin.register(PickAndMixBag)
class PickAndMixBagAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'max_weight_in_grams')
    filter_horizontal = ('sweets',)
