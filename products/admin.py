from django.contrib import admin
from django.utils.html import mark_safe
from .models import SweetCategory, DietaryTag, Product

# Register your models here.


@admin.register(SweetCategory)
class SweetCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    search_field = ('name',)


@admin.register(DietaryTag)
class DietaryTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    search_field = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'sku',
        'price',
        'sweet_category',
        'image',
        'in_stock',
    )
