from django.contrib import admin

from .models import SweetCategory

# Register your models here.


@admin.register(SweetCategory)
class SweetCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    search_field = ('name',)
