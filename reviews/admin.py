from django.contrib import admin
from .models import Review

# Register your models here.


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'rating',
        'approved',
        'created_at',
    )

    list_filter = (
        'created_at',
        'name',
    )

    ordering = ('-created_at',)
