# Standard libary imports
# Third-party imports
# Django imports
from django.contrib import admin
# Local imports
from .models import Order, OrderLineItem

# Register your models here.


class OrderLineItemInline(admin.TabularInline):
    """
    Inline admin display for an orders line item
    """
    model = OrderLineItem
    extra = 0
    fields = (
        'product',
        'pick_and_mix_bag',
        'pick_and_mix_item',
        'quantity',
        'line_item_total',
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Display admin interface for managing orders

    displays all listed fields
    """

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
        'order_fulfilled',
    )

    list_filter = ('date_time', 'order_fulfilled',)

    search_fields = (
        'order_number',
        'full_name',
        'email',
        'phone_number',
    )

    ordering = ('-date_time',)
