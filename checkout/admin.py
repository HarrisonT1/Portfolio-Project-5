from django.contrib import admin
from .models import Order, OrderLineItem

# Register your models here.


class OrderLineItemInline(admin.TabularInline):
    model = OrderLineItem
    extra = 0
    fields = ('product', 'quantity', 'pick_and_mix_bag')
    readonly_fields = ('line_item_total',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    inlines = [OrderLineItemInline]

    readonly_fields = (
        'order_number',
        'date_time',
    )

    list_display = (
        'full_name',
        'email',
        'phone_number',
        'order_number',
        'date_time',
        'country',
        'postcode',
        'city',
        'town',
        'street_address1',
        'street_address2',
        'delivery_method',
    )

    list_filter = ('date_time',)

    search_fields = (
        'order_number',
        'full_name',
        'email',
        'phone_number',
    )

    ordering = ('-date_time',)
