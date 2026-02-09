from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    save_info = forms.BooleanField(required=False, label='Save information for your next order')

    class Meta:
        model = Order
        fields = [
            'full_name',
            'email',
            'phone_number',
            'country',
            'postcode',
            'city',
            'town',
            'street_address1',
            'street_address2',
        ]
