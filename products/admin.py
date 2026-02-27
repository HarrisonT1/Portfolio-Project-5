# Standard libary imports
# Third-party imports
# Django imports
from django.contrib import admin
# Local imports
from .models import SweetCategory, DietaryTag, Product

# Register your models here.


@admin.register(SweetCategory)
class SweetCategoryAdmin(admin.ModelAdmin):
    """
    Registers sweetcategory tab in the admin
    """
    list_display = ('name', 'id')
    search_fields = ('name',)


@admin.register(DietaryTag)
class DietaryTagAdmin(admin.ModelAdmin):
    """
    Registers dietarytag tab in the admin
    """
    list_display = ('name', 'id')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Registers product tab in the admin
    """
    list_display = (
        'name',
        'id',
        'sku',
        'price',
        'sweet_category',
        'image',
        'in_stock',
        'stock_level',
    )

    list_editable = (
        'stock_level',
    )

    search_fields = (
        'name',
        'sku',
    )
