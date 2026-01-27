from django.contrib import admin
from .models import SweetCategory, DietaryTag, Product

# Register your models here.


@admin.register(SweetCategory)
class SweetCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    search_fields = ('name',)


@admin.register(DietaryTag)
class DietaryTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'id',
        'sku',
        'price',
        'sweet_category',
        'image',
        'in_stock',
    )

    search_fields = (
        'name',
        'sku',
    )
